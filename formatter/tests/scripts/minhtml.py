import htmlmin
import argparse

def minify_file(input_file: str, output_file: str):
    with open(input_file, 'r') as f:
        content = f.read()

    minified_content = htmlmin.minify(
        content,
        remove_comments=True,
        remove_all_empty_space=True,
    )

    with open(output_file, 'w') as f:
        f.write(minified_content)

    print(f"Minified {input_file} -> {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Minify HTML files")
    parser.add_argument('input_file', help="Path to the input HTML file")
    parser.add_argument('output_file', help="Path to save the minified HTML file")
    args = parser.parse_args()

    minify_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
