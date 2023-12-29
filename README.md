# tabular_page_maker

Makes tabular HTML pages from YAML.

Takes keyword arguments `--output` and `--stylesheet`, and a
positional argument to name the YAML input file.

The top two levels of the YAML file make an X-Y grid of table cells,
and any lower levels go into unordered lists iwthin those cells.

