import sys
from markitdown import MarkItDown

# input file path 
# first argument is the file path

# 检查是否提供了文件路径
if len(sys.argv) != 2:
    print("Usage: python3 ./pdftomd.py <path_to_pdf>")
    sys.exit(1)

pdf_path = sys.argv[1]

markitdown = MarkItDown()
result = markitdown.convert(pdf_path, preserve_formatting=True, include_images=True)
# print(result.text_content)
# write into md file
with open("output.md", "w") as f:
    f.write(result.text_content)

print("Conversion complete. Output written to output.md")
