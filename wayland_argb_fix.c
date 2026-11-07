#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdint.h>
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <Imlib2.h>
#include <cairo/cairo.h>
#include <cairo/cairo-xlib.h>

typedef int (*XSetForeground_fn)(Display *, GC, unsigned long);
typedef Colormap (*XCreateColormap_fn)(Display *, Window, Visual *, int);
typedef int (*XQueryColor_fn)(Display *, Colormap, XColor *);
typedef void *(*XftDrawCreate_fn)(Display *, Drawable, Visual *, Colormap);
typedef void (*imlib_render_fn)(int, int, int, int, int, int, int, int);

static Visual *g_argb_visual = NULL;
static Colormap g_argb_colormap = 0;

__attribute__((constructor))
static void conky_wayland_fix_init(void) {
    unsetenv("LD_PRELOAD");
}

Colormap XCreateColormap(Display *display, Window w, Visual *visual, int alloc) {
    static XCreateColormap_fn real_XCreateColormap = NULL;
    if (!real_XCreateColormap) {
        real_XCreateColormap = (XCreateColormap_fn)dlsym(RTLD_NEXT, "XCreateColormap");
    }
    Colormap cmap = real_XCreateColormap(display, w, visual, alloc);
    if (visual && cmap) {
        g_argb_visual = visual;
        g_argb_colormap = cmap;
    }
    return cmap;
}

int XQueryColor(Display *display, Colormap colormap, XColor *def_in_out) {
    static XQueryColor_fn real_XQueryColor = NULL;
    if (!real_XQueryColor) {
        real_XQueryColor = (XQueryColor_fn)dlsym(RTLD_NEXT, "XQueryColor");
    }
    if (colormap == 0 && g_argb_colormap != 0) {
        colormap = g_argb_colormap;
    }
    if (colormap == 0 && def_in_out) {
        unsigned long p = def_in_out->pixel;
        def_in_out->red = (unsigned short)(((p >> 16) & 0xff) * 0x0101);
        def_in_out->green = (unsigned short)(((p >> 8) & 0xff) * 0x0101);
        def_in_out->blue = (unsigned short)((p & 0xff) * 0x0101);
        def_in_out->flags = DoRed | DoGreen | DoBlue;
        return 1;
    }
    return real_XQueryColor(display, colormap, def_in_out);
}

void *XftDrawCreate(Display *dpy, Drawable drawable, Visual *visual, Colormap colormap) {
    static XftDrawCreate_fn real_XftDrawCreate = NULL;
    if (!real_XftDrawCreate) {
        real_XftDrawCreate = (XftDrawCreate_fn)dlsym(RTLD_NEXT, "XftDrawCreate");
    }
    if (!visual && g_argb_visual) {
        visual = g_argb_visual;
    }
    if (!colormap && g_argb_colormap) {
        colormap = g_argb_colormap;
    }
    if (g_argb_visual && !imlib_context_get_visual()) {
        imlib_context_set_visual(g_argb_visual);
        if (g_argb_colormap) {
            imlib_context_set_colormap(g_argb_colormap);
        }
    }
    return real_XftDrawCreate(dpy, drawable, visual, colormap);
}

int XSetRegion(Display *display, GC gc, Region r) {
    (void)display;
    (void)gc;
    (void)r;
    return 1;
}

int XftDrawSetClip(void *draw, Region r) {
    (void)draw;
    (void)r;
    return 1;
}

int XSetForeground(Display *display, GC gc, unsigned long foreground) {
    static XSetForeground_fn real_XSetForeground = NULL;
    if (!real_XSetForeground) {
        real_XSetForeground = (XSetForeground_fn)dlsym(RTLD_NEXT, "XSetForeground");
    }
    return real_XSetForeground(display, gc, foreground | 0xff000000UL);
}

void imlib_render_image_part_on_drawable_at_size(
    int source_x, int source_y, int source_width, int source_height,
    int destination_x, int destination_y, int destination_width, int destination_height)
{
    static imlib_render_fn real_render = NULL;
    if (!real_render) {
        real_render = (imlib_render_fn)dlsym(RTLD_NEXT, "imlib_render_image_part_on_drawable_at_size");
    }

    Display *dpy = imlib_context_get_display();
    Drawable drawable = imlib_context_get_drawable();
    Visual *visual = imlib_context_get_visual();
    if (!visual && g_argb_visual) {
        visual = g_argb_visual;
        imlib_context_set_visual(g_argb_visual);
        if (g_argb_colormap) {
            imlib_context_set_colormap(g_argb_colormap);
        }
    }
    Imlib_Image img = imlib_context_get_image();

    if (!dpy || !drawable || !visual || !img ||
        source_width <= 0 || source_height <= 0 ||
        destination_width <= 0 || destination_height <= 0) {
        if (real_render) {
            real_render(source_x, source_y, source_width, source_height,
                        destination_x, destination_y, destination_width, destination_height);
        }
        return;
    }

    int img_w = imlib_image_get_width();
    int img_h = imlib_image_get_height();
    DATA32 *data = imlib_image_get_data_for_reading_only();
    if (!data || source_x < 0 || source_y < 0 ||
        source_x + source_width > img_w || source_y + source_height > img_h) {
        if (real_render) {
            real_render(source_x, source_y, source_width, source_height,
                        destination_x, destination_y, destination_width, destination_height);
        }
        return;
    }

    uint32_t *premul = (uint32_t *)malloc((size_t)source_width * (size_t)source_height * sizeof(uint32_t));
    if (!premul) {
        return;
    }

    for (int y = 0; y < source_height; y++) {
        const DATA32 *src_row = data + (size_t)(source_y + y) * (size_t)img_w + source_x;
        uint32_t *dst_row = premul + (size_t)y * (size_t)source_width;
        for (int x = 0; x < source_width; x++) {
            uint32_t p = src_row[x];
            uint32_t a = (p >> 24) & 0xff;
            if (a == 0) {
                dst_row[x] = 0;
            } else if (a == 255) {
                dst_row[x] = p;
            } else {
                uint32_t r = (((p >> 16) & 0xff) * a + 127) / 255;
                uint32_t g = (((p >> 8) & 0xff) * a + 127) / 255;
                uint32_t b = ((p & 0xff) * a + 127) / 255;
                dst_row[x] = (a << 24) | (r << 16) | (g << 8) | b;
            }
        }
    }

    cairo_surface_t *dst_surf = cairo_xlib_surface_create(
        dpy, drawable, visual,
        destination_x + destination_width,
        destination_y + destination_height);
    cairo_surface_t *src_surf = cairo_image_surface_create_for_data(
        (unsigned char *)premul, CAIRO_FORMAT_ARGB32,
        source_width, source_height, source_width * 4);

    cairo_t *cr = cairo_create(dst_surf);
    cairo_translate(cr, destination_x, destination_y);
    if (destination_width != source_width || destination_height != source_height) {
        cairo_scale(cr, (double)destination_width / (double)source_width,
                        (double)destination_height / (double)source_height);
    }
    cairo_set_source_surface(cr, src_surf, 0, 0);
    cairo_paint(cr);

    cairo_destroy(cr);
    cairo_surface_flush(dst_surf);
    cairo_surface_destroy(src_surf);
    cairo_surface_destroy(dst_surf);
    free(premul);
}
