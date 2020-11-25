# this does the actual plugin registration, by putting `register` in namespace
from pelican.plugins.liquid_tags import register
from pelican.plugins.liquid_tags.mdx_liquid_tags import LiquidTags

def process_args(markup):
    attrs = {}
    kwargs = [line.strip() for line in markup.split('|')]
    for kwarg in kwargs:
        key, _, value = [_.strip() for _ in kwarg.partition('=')]
        if not value:
            if 'image_path' not in attrs:
                value = key
                key = 'image_path'
            else:
                value = True
        attrs[key] = value
    return attrs


def single_image(
    image_path=None,
    alt_text='',
    title_text='',
    caption='',
    display_caption=False,
    no_thumbnail=False,
    **kwargs
):
    caption_text = caption
    if display_caption and not caption_text:
        raise ValueError(f"{src}: display_caption without image description is invalid")

    image_stem, image_suffix = image_path.rsplit('.', 1)
    thumb_path = f"{image_stem}-min.{image_suffix}"
    if no_thumbnail:
        thumb_path = image_path

    if not title_text and caption_text:
        title_text = caption_text
    if title_text:
        title_text = f'title="{title_text}"'

    if not alt_text and caption_text:
        alt_text = caption_text
    if alt_text:
        alt_text = f'alt="{alt_text}"'

    figcaption = ""
    if display_caption:
        figcaption = f'<figcaption>{caption_text}</figcaption>'

    template = """
    <figure>
        <a href="{image_path}" target="_blank">
            <img src="{thumb_path}" {title_text} {alt_text} loading="lazy">
        </a>
        {figcaption}
    </figure>
    """

    return template.format(
        image_path=image_path,
        thumb_path=thumb_path,
        title_text=title_text,
        alt_text=alt_text,
        figcaption=figcaption
    ).strip()


@LiquidTags.register('figure')
def figure(preprocessor, tag, markup):
    """
    Generates img tag for thumbnail wrapped in link to full-sized file

    Syntax is:
    {% figure path_to_file [| display_caption] [|caption=image description] [|use_thumbnail] %}
    """
    if not markup:
        raise ValueError("{% figure %} requires filename")

    attrs = process_args(markup)

    return single_image(**attrs)


@LiquidTags.register('gallery')
def gallery(preprocessor, tag, markup):
    """
    Generates gallery of figures that have thumbnails wrapped in link to
    full-sized files, with optional captions

    Syntax is:
    {% gallery
        path_to_file [| display_caption] [|caption=image description]
        path_to_file [| display_caption] [|caption=image description]
    %}
    """
    if not markup:
        raise ValueError("{% gallery %} requires at least one image")

    images = []
    for image_markup in markup.split('\n'):
        attrs = process_args(image_markup)
        images.append(single_image(**attrs))

    return '<div class="gallery">\n{gallery}</div>'.format(gallery="\n".join(images))
