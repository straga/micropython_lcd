import lv_config_90 as lv_config
import lvgl as lv

HEIGHT  = lv_config.HEIGHT
WIDTH   = lv_config.WIDTH

size_x = 50
size_y = 50
slide_x = 200
slide_y = 40
text_y = -100

# LVGL TEST
import task_handler
th = task_handler.TaskHandler()

print('Hello LVGL')

scr = lv.screen_active()
scr.set_style_bg_color(lv.color_hex(0x000000), 0)

print('Left TOP')
# Left TOP
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(0, 0)
rect.set_style_bg_color(lv.color_make(255, 0, 0), 0) # red

# Добавляем букву R внутри красного квадрата
label = lv.label(rect)
label.set_text("R")
label.center()  # Центрируем букву в квадрате
label.set_style_text_color(lv.color_make(0, 0, 0), 0)  # Белый цвет для текста
label.set_style_text_font(lv.font_montserrat_16, 0)  # Larger font


print('Right TOP')
# Right TOP
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(WIDTH-size_x, 0)
rect.set_style_bg_color(lv.color_make(0, 255, 0), 0) # green

# Добавляем букву R внутри красного квадрата
label = lv.label(rect)
label.set_text("G")
label.center()  # Центрируем букву в квадрате
label.set_style_text_color(lv.color_make(0, 0, 0), 0)  # Белый цвет для текста
label.set_style_text_font(lv.font_montserrat_16, 0)  # Larger font


print('Left BOTTOM')
# Left BOTTOM
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(0, HEIGHT-size_y)
rect.set_style_bg_color(lv.color_make(0, 0, 255), 0) # blue

# Добавляем букву R внутри красного квадрата
label = lv.label(rect)
label.set_text("B")
label.center()  # Центрируем букву в квадрате
label.set_style_text_color(lv.color_make(0, 0, 0), 0)  # Белый цвет для текста
label.set_style_text_font(lv.font_montserrat_16, 0)  # Larger font

print('Right BOTTOM')
# Right BOTTOM
rect = lv.obj(scr)
rect.set_size(size_x, size_y)
rect.set_pos(WIDTH-size_x, HEIGHT-size_y)
rect.set_style_bg_color(lv.color_make(255, 255, 255), 0) # white

# Добавляем букву R внутри красного квадрата
label = lv.label(rect)
label.set_text("W")
label.center()  # Центрируем букву в квадрате
label.set_style_text_color(lv.color_make(0, 0, 0), 0)  # Белый цвет для текста
label.set_style_text_font(lv.font_montserrat_16, 0)  # Larger font


# Draw cross lines from inner corners to inner corners
line1 = lv.line(scr)
line2 = lv.line(scr)

# Define points for the lines
points1 = [
    {"x": size_x, "y": size_y},                  # Inner top-left corner
    {"x": WIDTH - size_x, "y": HEIGHT - size_y}  # Inner bottom-right corner
]
points2 = [
    {"x": WIDTH - size_x, "y": size_y},          # Inner top-right corner
    {"x": size_x, "y": HEIGHT - size_y}          # Inner bottom-left corner
]

# Set the points for the lines
line1.set_points(points1, 2)
line2.set_points(points2, 2)

# Set line colors (white in this case)
line1.set_style_line_color(lv.color_make(255, 255, 255), 0)
line2.set_style_line_color(lv.color_make(255, 255, 255), 0)

# Set line width
line1.set_style_line_width(2, 0)
line2.set_style_line_width(2, 0)
#
#
# Slider
slider = lv.slider(scr)
slider.set_size(slide_x, slide_y)
slider.center()

label = lv.label(scr)
label.set_text(f"{WIDTH}x{HEIGHT}")
label.align(lv.ALIGN.CENTER, 0, text_y)
label.set_style_text_font(lv.font_montserrat_16, 0)
