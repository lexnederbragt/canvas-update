import sys
import argparse
from api import get_course, split_url, page_exists

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Add a new page to canvas with the content of an html file.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The url of the course, ending with the course id", required = True)
    required_named.add_argument("-t", "--title", help="The title the page to be added, enclosed in quotation marks if it \
    contains one or more spaces. Note that the url of the page will be the title in lower case, with each space replaced by a dash", required = True)
    required_named.add_argument("-f", "--html_file", help="The path to the html file that contains the content of the page", required = True)
    parser.add_argument("-p", "--publish", help="Publish the page on Canvas at the time of creation (default: leave unpublished)", action='store_true')
    parser.add_argument("--force", help="If the page is already present, create the page anyway (default: off)", action='store_true')
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def create_page(course, title, html_content, published):
    new_page = course.create_page(wiki_page = {
        "title":title,
        "body":html_content,
        "published":published
        })
    return new_page

def main(args):
    args = parse_args(args)

    # check whether page needs to be published
    published = 'false'
    if args.publish:
        published = 'true'

    # extract course information from url and get course
    API_URL, course_id, new_page_name = split_url(args.url, expected = 'url only')
    course =  get_course(API_URL, course_id, args.config_file)

    # test whether page exists
    new_page_name = args.title.lower().replace(" ","-")
    if page_exists(course, new_page_name) and not args.force:
        message ="Error: page '{}' already exists on Canvas.\n".format(new_page_name)
        message += "Full url: {}\n".format(args.url)
        message += "To create anyway, use '--force'\n"
        sys.exit(message)

    # read new page content
    with open(args.html_file, 'r') as html_file:
        html_content = html_file.read()#.replace('\n', '')

    # update the course page
    new_page = create_page(course, args.title, html_content, published)
    print("Sucessfully added page '%s'. Full url: '%s'." \
        %(new_page.title, API_URL + '/courses/' + course_id + '/pages/' + new_page.url))

if __name__ == "__main__":
    main(sys.argv[1:])
