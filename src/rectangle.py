import PIL
from PIL import Image, ImageColor, ImageDraw


def draw_bbox(image, x_min, y_min, x_max, y_max, **kwargs):
    draw = ImageDraw.Draw(image, 'RGBA')
    draw.rectangle(xy=[(x_min, y_min), (x_max, y_max)], **kwargs)
    return image


def draw_frame(image, annotation, cmap_lambda=None, **kwargs):
    im = image.copy()
    an = annotation
    x_, y_, w_, h_ = (
        an[k] for k in ['bbox_left', 'bbox_top', 'bbox_width', 'bbox_height'])
    cmap = cmap_lambda(an)
    if cmap:
        outline_ = cmap['outline']
        fill_ = cmap['fill']
        for x, y, w, h, fill, outline in zip(x_, y_, w_, h_, fill_, outline_):
            im = draw_bbox(im,
                           x,
                           y,
                           x + w,
                           y + h,
                           fill=fill,
                           outline=outline,
                           **kwargs)
    else:
        for x, y, w, h in zip(x_, y_, w_, h_):
            im = draw_bbox(im, x, y, x + w, y + h, **kwargs)
    return im


def colormap(annotation, num_category, lightness=0.5):
    p_ = annotation['score']
    c_ = annotation['object_category']
    t_ = annotation['truncation']
    o_ = annotation['occlusion']

    C = num_category

    HUE = [x / C * 360 for x in range(C)]

    # fraction of the object in the image
    f_ = [max(0.0, t, o / 2) for t, o in zip(t_, o_)]

    # use fill alpha for occlusion or 1 - f
    max_fill_alpha = 0.25
    fill_alpha_ = [max_fill_alpha * f * 255 for f in f_]

    # use outline alpha for confidence
    max_outline_alpha = 0.75
    outline_alpha_ = [max_outline_alpha * p * 255 for p in p_]

    hue_ = [HUE[int(c)] for c in c_]
    # use saturation for confidence

    max_saturation = 75
    sat_ = [p * max_saturation for p in p_]
    l = lightness * 100

    rgb_ = [
        ImageColor.getcolor(f"hsl({h}, {s}%, {l}%)", 'RGB')
        for h, s in zip(hue_, sat_)
    ]

    outline_ = [rgb + (int(a), ) for rgb, a in zip(rgb_, outline_alpha_)]
    fill_ = [rgb + (int(a), ) for rgb, a in zip(rgb_, fill_alpha_)]

    return {'outline': outline_, 'fill': fill_}
