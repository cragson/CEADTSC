# author: cragson/ calb

from time import time

def read_shellcode_from_file( _file ):
    ret = []
    
    with open( _file, 'r+' ) as f:
        
        lines = f.readlines()
        
        for line in lines:
            if( line.strip() == '' ):
                continue
            else:
                ret.append( line )
    f.close()
    
    return ret

def make_vector( _lines ):
    ret = [ 'std::vector< uint8_t > m_shellcode =\n', '{\n' ]
    last_addr = 0
    
    for i in range( 0, len( _lines ), 1 ):
        
        if( _lines[ i ].strip() == '' ):
            continue
        
        line = _lines[ i ].rstrip()

        current_addr = int( line[ : line.find( ' ' ) ], 16 )

        if( i == 0 and last_addr == 0 ):
            last_addr = current_addr

        current_offset = current_addr - last_addr

        idx_1 = line.find( '-' )

        idx_2 = line.find( '-', idx_1 + 1 )

        bytes_raw = line[ idx_1 + 1 : idx_2 ].strip().replace( ' ', '' )

        instr = line[ idx_2 + 1 : ].rstrip()

        bytes_vec = ''
        
        for j in range( 0, len( bytes_raw ), 1 ):
            if( j == 0 ):
                bytes_vec += '0x'
                
            if( j % 2 == 0 and j > 0 ):
                bytes_vec += ', 0x' + bytes_raw[ j ]
            else:
                bytes_vec += bytes_raw[ j ]

            if( j == len( bytes_raw ) - 1 and i != len( _lines ) -1 ):
                bytes_vec += ','
                
        final_offset = '// ' + '{0:0{1}X}'.format( current_offset, 4 )

        ret.append( '\t\t' + '{:{align}{width}}'.format( bytes_vec, align='<', width='35' ) + final_offset + ' ' + instr + '\n' )

        if( i == len( _lines ) - 1 ):
            ret.append( '};' )

    return ret
        
def write_output_file( _lines ):
    name = 'sh_' + str( time() ).replace( '.', '' ) + '.txt'
    with open( name, 'w' ) as f:
        for line in _lines:
            f.write( line )
    f.close()

def main():
    file_name = input( "[-] Please enter the complete file name (e.g. 'awesomeshellz.txt'): ")
    ret = make_vector( read_shellcode_from_file( file_name ) )
    write_output_file( ret )
    print( ''.join( ret ) )

if __name__ == '__main__':
    main()
