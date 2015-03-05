from ferris import Controller, messages, route_with, route

import json



class Main(Controller):
    
        
    @route_with('/jmeroy', methods=['GET'])
    def show(self):
        self.meta.view.template_name = 'angular/index.html'
