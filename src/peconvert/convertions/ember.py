import hashlib
import pefile
from .helper import (
    calculate_entropy, 
    extract_ascii_strings,
    extract_unicode_strings
)

def convert(data: bytearray, filename: str):
    pe = pefile.PE(data=data, fast_load=False) 
    features = {}
    features['file_metadata'] = {
        'filename': filename,
        'size': len(data),
        'is_dll': bool(pe.FILE_HEADER.Characteristics & 0x2000),
        'is_executable': bool(pe.FILE_HEADER.Characteristics & 0x0002),
        'is_64bit': pe.FILE_HEADER.Machine == 0x8664,
    }
    features['file_hashes'] = {
        'md5': hashlib.md5(data).hexdigest(),
        'sha1': hashlib.sha1(data).hexdigest(),
        'sha256': hashlib.sha256(data).hexdigest(),
    }
    features['dos_header'] = {
        'magic': pe.DOS_HEADER.e_magic,
        'lfanew': pe.DOS_HEADER.e_lfanew,
    }
    header = pe.FILE_HEADER
    features['pe_header'] = {
        'machine': header.Machine,
        'number_of_sections': header.NumberOfSections,
        'timestamp': header.TimeDateStamp,
        'pointer_to_symbol_table': header.PointerToSymbolTable,
        'number_of_symbols': header.NumberOfSymbols,
        'size_of_optional_header': header.SizeOfOptionalHeader,
        'characteristics': header.Characteristics,
    }
    opt_header = pe.OPTIONAL_HEADER
    features['optional_header'] = {
            'magic': opt_header.Magic,
            'major_linker_version': opt_header.MajorLinkerVersion,
            'minor_linker_version': opt_header.MinorLinkerVersion,
            'size_of_code': opt_header.SizeOfCode,
            'size_of_initialized_data': opt_header.SizeOfInitializedData,
            'size_of_uninitialized_data': opt_header.SizeOfUninitializedData,
            'address_of_entry_point': opt_header.AddressOfEntryPoint,
            'base_of_code': opt_header.BaseOfCode,
            'image_base': opt_header.ImageBase,
            'section_alignment': opt_header.SectionAlignment,
            'file_alignment': opt_header.FileAlignment,
            'major_operating_system_version': opt_header.MajorOperatingSystemVersion,
            'minor_operating_system_version': opt_header.MinorOperatingSystemVersion,
            'size_of_image': opt_header.SizeOfImage,
            'size_of_headers': opt_header.SizeOfHeaders,
            'checksum': opt_header.CheckSum,
            'subsystem': opt_header.Subsystem,
            'dll_characteristics': opt_header.DllCharacteristics,
        }
    sections = []
    for section in pe.sections:
        sections.append({
            'name': section.Name.rstrip(b'\x00').decode('ascii', errors='ignore'),
            'virtual_size': section.Misc_VirtualSize,
            'virtual_address': section.VirtualAddress,
            'size_of_raw_data': section.SizeOfRawData,
            'pointer_to_raw_data': section.PointerToRawData,
            'characteristics': section.Characteristics,
            'entropy': calculate_entropy(
                data[section.PointerToRawData:section.PointerToRawData + section.SizeOfRawData]
            ),
        })
    features['sections'] = sections
    imports = {}
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        for dll in pe.DIRECTORY_ENTRY_IMPORT:
            dll_name = dll.dll.decode('ascii', errors='ignore')
            imports[dll_name] = []
            for imp in dll.imports:
                if imp.name:
                    imports[dll_name].append(imp.name.decode('ascii', errors='ignore'))
    features['imports'] = imports
    exports = []
    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            if exp.name:
                exports.append({
                    'name': exp.name.decode('ascii', errors='ignore'),
                    'ordinal': exp.ordinal,
                    'address': exp.address,
                })
    features['exports'] = exports
    resources = {
        'has_resources': False,
        'resource_types': [],
        'version_info': {}
    }
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        resources['has_resources'] = True
        # Count resource types
        try:
            for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
                resources['resource_types'].append(entry.struct.Id)
        except:
            pass
        
        # Try to extract version info
        try:
            if hasattr(pe, 'VS_FIXEDFILEINFO'):
                resources['version_info'] = {
                    'fixed_file_info': str(pe.VS_FIXEDFILEINFO)
                }
        except:
            pass
    
    features['resources'] = resources
    strings = {
        'ascii_strings': [],
        'unicode_strings': [],
        'suspicious_strings': []
    }
    ascii_strings = extract_ascii_strings(data)
    strings['ascii_strings'] = list(set(ascii_strings))[:50]  # Limit to 50 unique strings
    
    # Extract Unicode strings
    unicode_strings = extract_unicode_strings(data)
    strings['unicode_strings'] = list(set(unicode_strings))[:50]
    
    # Look for suspicious patterns
    suspicious_patterns = [
        'CreateRemoteThread', 'VirtualAllocEx', 'WriteProcessMemory',
        'GetModuleHandle', 'GetProcAddress', 'ShellExecute',
        'WinExec', 'CreateProcess', 'TerminateProcess',
        'ReadProcessMemory', 'SetWindowsHookEx', 'RegOpenKey',
        'RegSetValue', 'FindFirstFile', 'InternetOpen',
        'URLDownloadToFile', 'HttpSendRequest', 'WinINet'
    ]
    
    all_strings = ascii_strings + unicode_strings
    for pattern in suspicious_patterns:
        if any(pattern.lower() in s.lower() for s in all_strings):
            strings['suspicious_strings'].append(pattern)
    
    features['strings'] = strings

    debug_info = {
        'has_debug_directory': False,
        'debug_entries': []
    }
    if hasattr(pe, 'DIRECTORY_ENTRY_DEBUG'):
        debug_info['has_debug_directory'] = True
        try:
            for entry in pe.DIRECTORY_ENTRY_DEBUG:
                debug_info['debug_entries'].append({
                    'type': entry.struct.Type,
                    'size': entry.struct.SizeOfData,
                    'address': entry.struct.AddressOfRawData,
                })
        except:
            pass
    features['debug_info'] = debug_info

    reloc_info = {
        'has_reloc_directory': False,
        'relocation_size': 0
    }
    if hasattr(pe, 'DIRECTORY_ENTRY_BASERELOC'):
            reloc_info['has_reloc_directory'] = True
            reloc_info['relocation_size'] = len(pe.DIRECTORY_ENTRY_BASERELOC)
        
    features['relocation_info'] = reloc_info

    tls_info = {
        'has_tls': False,
        'tls_callbacks': 0
    }

    if hasattr(pe, 'DIRECTORY_ENTRY_TLS'):
        tls_info['has_tls'] = True
        try:
            tls_info['tls_callbacks'] = len(pe.DIRECTORY_ENTRY_TLS.callbacks)
        except:
            pass
        
    features['tls_info'] = tls_info
    return features