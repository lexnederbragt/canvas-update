import sys
import argparse
from api import get_course, split_url

def parse_args(args):
    # help text and argument parser
    # solution based on https://stackoverflow.com/a/24181138/462692
    desc = '\n'.join(["Lists the modules with position, name and url for a course on Canvas in the order in which they appear.",
                     "An optional argument -c/--config_file can be used with the path to the config file. "
                     "Otherwise the default config file '~/.config/canvasapi.conf' will be used.\n"
                      ])
    parser = argparse.ArgumentParser(description=desc)
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-u", "--url", help="The url of the course, ending with the course id", required = True)
    parser.add_argument("-cf", "--config_file", help="Path to config file", default = '~/.config/canvasapi.conf')
    args = parser.parse_args(args)
    return args

def get_module_url(module_items_url):
    """
    Extracts the module direct url from the items_url.
    Example:
    items_url https://canvas.instance.com/api/v1/courses/course_id/modules/module_id/items'
    becomes https://canvas.instance.com/courses/course_id/modules/module_id
    """
    return module_items_url.replace('api/v1/','').replace('/items', '')

def main(args):
    args = parse_args(args)

    # extract course information from url and get course
    API_URL, course_id, new_folder_name = split_url(args.url, expected = 'url only')
    course =  get_course(API_URL, course_id, args.config_file)

    modules = {}
    for module in course.get_modules():
        module_url = get_module_url(module.items_url)
        modules[module.position] = { "name" : module.name,
                                    "items" : module_url,
                                    "published" : module.published
                                    }
    print("Position\tModule name\tModule url\tPublished")
    for position in sorted(modules.keys()):
        module = modules[position]
        print(f"{position}\t{module['name']}\t{module['items']}\t{module['published']}")

if __name__ == "__main__":
    main(sys.argv[1:])
