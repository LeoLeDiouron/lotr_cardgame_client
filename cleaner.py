class Cleaner:

    @staticmethod
    def clean_menu(app):
        '''
        '''

        app.background_menu.destroy()
        app.button_play.destroy()
        app.button_exit.destroy()

    @staticmethod
    def clean_wait_player(app, function):
        '''
        '''

        app.background_wait_player.cancel(function)
        app.background_wait_player.destroy()
        app.img_waiting.destroy()
        app.button_exit.destroy()
    
    @staticmethod
    def clean_choose_faction(app):
        '''
        '''

        app.background_faction.destroy()
        app.button_faction_1.destroy()
        app.button_faction_2.destroy()
        app.button_faction_3.destroy()
        app.button_faction_4.destroy()
    
    @staticmethod
    def clean_wait_begin(app, function):
        '''
        '''

        app.background_wait_begin.cancel(function)
        app.background_wait_begin.destroy()
    
    @staticmethod
    def clean_slot_descriptions(app):
        '''
        '''

        app.card_img_big.destroy()
        app.name_card.destroy()
        app.description_card.destroy()
        app.description_power_card.destroy()
