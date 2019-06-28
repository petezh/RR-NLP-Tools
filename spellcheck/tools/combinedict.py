
def main():

    outfile_unicode = open('sci_unicode.txt','w', encoding="utf-8")
    outfile_acsii = open('sci_ascii.txt','w')
    infile = open("dict_sci.txt","r", errors= 'ignore', encoding="utf-8")
    
    for s in infile:
        
        if is_ascii(s):
            outfile_acsii.write(s)

        else:
            outfile_unicode.write(s)

def is_ascii(s):
    return all(ord(c) < 128 for c in s)


if __name__ == "__main__":
    main()

