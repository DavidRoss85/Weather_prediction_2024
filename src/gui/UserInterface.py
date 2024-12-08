import copy

from src.gui.Graph import GraphGUI
from src.gui.Window_GUI import Window
from src.model.g_naive_bayes import NaiveBayesModel
from src.model.structures import DataSet, Range


class UserInterface:
    LOCATION_TITLE='COUNTY'
    TEMPERATURE_TITLE='TAVG'
    WIND_TITLE='AWND'
    PRECIP_TITLE='PRCP'
    def __init__(self):
        self.__main_window=Window("Crop Weather predictor",1024,768)
        self.__main_frame=Window.Frame("mainFrame",1024,768,0,0,)

        self.__location_variable=Window.StringVar()
        self.__location_options=[]

        self.__crop_variable=Window.StringVar()
        self.__crop_options=[]

        self.__temp_checked=Window.IntVar()
        self.__prcp_checked=Window.IntVar()
        self.__wind_checked=Window.IntVar()

        self.__main_data=None
        self.__temp_data=None
        self.__prcp_data=None
        self.__wind_data=None

        self.__temp_model=NaiveBayesModel()
        self.__prcp_model=NaiveBayesModel()
        self.__wind_model=NaiveBayesModel()

        self.__temp_range=Range(20,55)
        self.__prcp_range=Range(0,1,0.01)
        self.__wind_range=Range(0,5,0.01)

        self.__graph=GraphGUI("Condition Probabilities","Day of Year","Likelihood")




        # Generate window:
        self.__put_things_in_window()
        self.__main_window.add_widget(self.__main_frame)

    def display_predictions(self):
        self.__import_data()
        self.filter_data('CHELAN')
        self.train_models()
        self.get_predictions()
        self.show_graph()


    def show(self):
        self.__main_window.display_window()

    def __put_things_in_window(self):
        # Generate widgets and attach to frame:
        self.__create_comboboxes()
        self.__create_labels()
        self.__create_buttons()
        self.__create_text_fields()

    def __create_text_fields(self):
        # Generate a text field for minutes
        t1 = Window.TextBox("txtMinutes", 5, 1, 285, 0)

        # Attach function to text box
        t1.on_keyup = lambda window, args: print("")

        # and attach to frame
        self.__main_frame.add_widget(t1)

    def __create_labels(self):
        # generate a big label
        big_label = Window.Label("lblTitle", "Calculate long distance rates:", 40, 1, -50, 50)
        big_label.forecolor = "red"
        big_label.font_size = 30

        # Attach to main window:
        self.__main_window.add_widget(big_label)

        # generate label for cost
        l1 = Window.Label("lblAnswer", "-", 17, 0, 100, 75)
        l2 = Window.Label("lblMinutes", "  Enter Total Minutes:", 17, 0, 0, 0)

        # and attach to frame
        self.__main_frame.add_widget(l1)
        self.__main_frame.add_widget(l2)

    def __create_buttons(self):
        # Generate Exit button:
        b1 = Window.Button("btnExit", "Exit", 10, 1, 170, 320)
        b2 = Window.Button("btnExecute", "Execute", 10, 1, 170, 420)

        # Attach functions to buttons:
        b1.on_click = lambda window, args: self.__main_window.exit()
        b2.on_click = lambda window, args: self.display_predictions()

        # Attach buttons to frame
        self.__main_frame.add_widget(b1)
        self.__main_frame.add_widget(b2)

    def __create_comboboxes(self):
        location_choice=Window.ComboBox("cmbLocation",["Select"],0, 11,1,20,100)



    # =================================Data Processing========================================
    def __import_data(self):
        datafile="../data/final_combined_data.csv"

        self.__main_data=DataSet("Everything","../data/final_combined_data.csv")
        self.__crop_options=self.__main_data.get_category_list('COUNTY')

        my_data=copy.deepcopy(self.__main_data)
        self.__temp_data= self.__prepare_data(my_data)
        self.__wind_data= self.__prepare_data(my_data)
        self.__prcp_data= self.__prepare_data(my_data)



    def __prepare_data(self,dataset):
        d=copy.deepcopy(dataset)
        d.drop_data("SOURCE_FILE")
        d.drop_data("VALUE")
        d.drop_data('COMMODITY')
        d.drop_duplicates()
        d.drop_duplicates(['YEAR', 'COUNTY', 'DATE'], ['TAVG', 'TMAX', 'TMIN', 'PRCP', 'AWND', 'SNOW'])
        d.convert_dates_to_julian('DATE')
        d.sort_data(['YEAR'])

        return d

    def filter_data(self,location:str=None):
        location_field='COUNTY'
        if location:
            self.__temp_data.filter_data(location_field,location)
            self.__wind_data.filter_data(location_field,location)
            self.__prcp_data.filter_data(location_field,location)

        #Temperature settings
        self.__temp_data.replace_nan_using_avg('TAVG',['TMAX','TMIN'])
        self.__temp_data.drop_nan_values(['TAVG'])
        self.__temp_data.set_features(['TAVG'])
        self.__temp_data.set_labels('DATE')
        self.__temp_data.input_ranges=[self.__temp_range]
        self.__temp_data.set_name("Temperature")
        self.__temp_data.set_graph_color("black","red")
        # self.__temp_data.set_scale(1)

        #Precipitation settings
        self.__prcp_data.drop_nan_values(['PRCP'])
        self.__prcp_data.set_features(['PRCP'])
        self.__prcp_data.set_labels('DATE')
        self.__prcp_data.input_ranges = [self.__prcp_range]
        self.__prcp_data.set_name("Precipitation")
        self.__prcp_data.set_graph_color("black","blue")

        #Wind Settings
        self.__wind_data.drop_nan_values(['AWND'])
        self.__wind_data.set_features(['AWND'])
        self.__wind_data.set_labels('DATE')
        self.__wind_data.input_ranges = [self.__wind_range]
        self.__wind_data.set_name("Wind")
        self.__wind_data.set_graph_color("black","green")

    def train_models(self):
        self.__temp_model.train_model(self.__temp_data)
        self.__prcp_model.train_model(self.__prcp_data)
        self.__wind_model.train_model(self.__wind_data)

    def get_predictions(self):
        self.__temp_data=self.__temp_model.run_prediction(self.__temp_data)
        self.__prcp_data=self.__prcp_model.run_prediction(self.__prcp_data)
        self.__wind_data=self.__wind_model.run_prediction(self.__wind_data)

    def show_graph(self):
        self.__temp_data.gaussify()
        self.__prcp_data.gaussify()
        self.__wind_data.gaussify()
        
        self.__graph.add_graph(self.__temp_data.graph)
        self.__graph.add_graph(self.__prcp_data.graph)
        self.__graph.add_graph(self.__wind_data.graph)

        self.__graph.show()
