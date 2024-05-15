from vk_api.keyboard import VkKeyboard, VkKeyboardColor

main_menu_keyboard = VkKeyboard()
main_menu_keyboard.add_button('Старт', color=VkKeyboardColor.POSITIVE)
main_menu_keyboard.add_line()
main_menu_keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
main_menu_keyboard.add_button('Мои результаты', color=VkKeyboardColor.POSITIVE)
