import copy

from src.gui.Graph import GraphGUI
from src.gui.Window_GUI import Window
from src.model.g_naive_bayes import NaiveBayesModel
from src.model.structures import DataSet, Range
from src.utils.input_validation import validate_float


class UserInterface:
    LOCATION_TITLE='COUNTY'
    TEMPERATURE_TITLE='TAVG'
    WIND_TITLE='AWND'
    PRECIP_TITLE='PRCP'
    LOCATION_DEFAULT_TEXT = "Select a location"

    def __init__(self):
        self.__main_window=Window("Crop Weather predictor",1024,768)
        self.__main_frame=Window.Frame("mainFrame",1024,768,0,0,)

        self.__location_variable=Window.StringVar()
        self.__location_options=[]
        self.__location_to_use=None

        self.__crop_variable=Window.StringVar()
        self.__crop_dict=dict()
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

        self.__import_data()

        # Generate window:
        self.__put_things_in_window()
        self.__main_window.add_widget(self.__main_frame)


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
        t1 = Window.TextBox("txtTempMin", 5, 1, 350, 300)
        t2 = Window.TextBox("txtTempMax", 5, 1, 450, 300)
        t3 = Window.TextBox("txtPrcpMin", 5, 1, 350, 350)
        t4 = Window.TextBox("txtPrcpMax", 5, 1, 450, 350)
        t5 = Window.TextBox("txtWindMin", 5, 1, 350, 400)
        t6 = Window.TextBox("txtWindMax", 5, 1, 450, 400)

        # Attach function to text box
        t1.on_keyup = lambda window, args: self.set_values()
        t2.on_keyup = lambda window, args: self.set_values()
        t3.on_keyup = lambda window, args: self.set_values()
        t4.on_keyup = lambda window, args: self.set_values()
        t5.on_keyup = lambda window, args: self.set_values()
        t6.on_keyup = lambda window, args: self.set_values()

        # and attach to frame
        self.__main_frame.add_widget(t1)
        self.__main_frame.add_widget(t2)
        self.__main_frame.add_widget(t3)
        self.__main_frame.add_widget(t4)
        self.__main_frame.add_widget(t5)
        self.__main_frame.add_widget(t6)

    def __create_labels(self):
        # generate a big label
        big_label = Window.Label("lblTitle", "Input settings", 40, 1, -50, 50)
        big_label.forecolor = "red"
        big_label.font_size = 30

        # Attach to main window:
        self.__main_window.add_widget(big_label)

        # generate labels for variables
        l1 = Window.Label("lblTemp", "Temperature:", 17, 0, 100, 300)
        l2 = Window.Label("lblPrcp", "Precipitation:", 17, 0, 100, 350)
        l3 = Window.Label("lblWind", "Wind Speed:", 17, 0, 100, 400)

        l4 = Window.Label("lblMin", "Min", 5, 0, 350, 250)
        l5 = Window.Label("lblMax", "Max", 5, 0, 450, 250)

        # and attach to frame
        self.__main_frame.add_widget(l1)
        self.__main_frame.add_widget(l2)
        self.__main_frame.add_widget(l3)
        self.__main_frame.add_widget(l4)
        self.__main_frame.add_widget(l5)

    def __create_buttons(self):
        # Generate Exit button:
        b1 = Window.Button("btnExit", "Exit", 10, 1, 350, 450)
        b2 = Window.Button("btnExecute", "Execute", 10, 1, 150, 450)

        # Attach functions to buttons:
        b1.on_click = self.__main_window.exit
        b2.on_click = self.display_predictions

        # Attach buttons to frame
        self.__main_frame.add_widget(b1)
        self.__main_frame.add_widget(b2)

    def __create_comboboxes(self):
        crop_box=Window.ComboBox("cmbCrop", self.__crop_options, 0, 20, 1, 100, 100)
        location_box=Window.ComboBox("cmbLocation",self.__location_options,0, 20,1,100,150)

        #Attach functions:
        crop_box.on_click= lambda window,args: self.set_values()
        location_box.on_click= lambda window,args: self.set_values()
        crop_box.on_select = lambda window, args: self.populate_values()
        location_box.on_select = lambda window, args: self.set_values()

        #Settings:
        self.__crop_variable.set("Select a crop")
        crop_box.variable=self.__crop_variable
        self.__location_variable.set(self.LOCATION_DEFAULT_TEXT)
        location_box.variable=self.__location_variable

        #Attach to frame
        self.__main_frame.add_widget(crop_box)
        self.__main_frame.add_widget(location_box)

    # =================================Data Processing========================================
    def display_predictions(self):
        self.__import_data()
        self.reset_models()
        self.filter_data(self.__location_to_use)
        self.train_models()
        self.get_predictions()
        self.show_graph()

    def reset_models(self):
        self.__temp_model.reset_model()
        self.__prcp_model.reset_model()
        self.__wind_model.reset_model()
        
    def populate_values(self):
        crop=self.__crop_variable.get()
        put=self.__main_frame.set_text_value
        if crop in self.__crop_dict:
            entry=self.__crop_dict[crop]
            put("txtTempMin",entry['TAVG_MIN'])
            put("txtTempMax", entry['TAVG_MAX'])
            put("txtPrcpMin", entry['PRCP_MIN'])
            put("txtPrcpMax", entry['PRCP_MAX'])
            put("txtWindMin", entry['AWND_MIN'])
            put("txtWindMax", entry['AWND_MAX'])

        self.set_values()

    def set_values(self):
        location=self.__location_variable.get()
        if not location or location==self.LOCATION_DEFAULT_TEXT:
            self.__location_to_use=None
        else:
            self.__location_to_use=location



        val=self.__main_frame.get_text_value
        flt=validate_float

        t_min=flt(val("txtTempMin"))["value"]
        t_max=flt(val("txtTempMax"))["value"]
        self.__temp_range=Range(t_min,t_max,1)

        p_min=flt(val("txtPrcpMin"))["value"]
        p_max=flt(val("txtPrcpMax"))["value"]
        self.__prcp_range=Range(p_min,p_max,0.01)

        w_min=flt(val("txtWindMin"))["value"]
        w_max=flt(val("txtWindMax"))["value"]
        self.__wind_range=Range(w_min,w_max,0.01)

        print(f"LOCATION SET TO: {location}")
        print(f"P_MIN: {p_min}")


    def __import_data(self):
        datafile="../data/final_combined_data.csv"
        cropfile="../data/crop_conditions_updated.csv"

        self.__main_data=DataSet("Everything",datafile)
        crop_data=DataSet("Crops",cropfile)

        my_data=copy.deepcopy(self.__main_data)
        self.__temp_data= self.__prepare_data(my_data)
        self.__wind_data= self.__prepare_data(my_data)
        self.__prcp_data= self.__prepare_data(my_data)

        self.__location_options=self.__main_data.get_category_list('COUNTY')
        self.__crop_dict=crop_data.get_dictionary_from_data('Commodity')
        self.__crop_options=[key for key in self.__crop_dict]


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
        tm=self.__temp_model
        td=self.__temp_data

        pm=self.__prcp_model
        p_d=self.__prcp_data

        wm=self.__wind_model
        wd=self.__wind_data

        if not td.is_empty():
            tm.train_model(td)
        else:
            self.__main_window.show_message(
                "No data available for the specified temperatures and location.",
                title="Empty Dataset"
            )

        if not p_d.is_empty():
            pm.train_model(p_d)
        else:
            self.__main_window.show_message(
                "No data available for the specified temperatures and location.",
                title="Empty Dataset"
            )

        if not wd.is_empty():
            wm.train_model(wd)

    def get_predictions(self):
        tm=self.__temp_model
        td=self.__temp_data

        pm=self.__prcp_model
        p_d=self.__prcp_data

        wm=self.__wind_model
        wd=self.__wind_data

        if tm.is_trained():
            td=tm.run_prediction(td)
        if pm.is_trained():
            p_d=pm.train_model(p_d)
        if wm.is_trained():
            wd=wm.train_model(wd)


    def show_graph(self):
        self.__temp_data.gaussify()
        self.__prcp_data.gaussify()
        self.__wind_data.gaussify()

        self.__graph.add_graph(self.__temp_data.graph)
        self.__graph.add_graph(self.__prcp_data.graph)
        self.__graph.add_graph(self.__wind_data.graph)

        self.__graph.show()
