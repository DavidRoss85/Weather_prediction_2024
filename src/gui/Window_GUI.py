import tkinter as tk
from tkinter import ttk

class _Parent:
    """
    Abstract class
    Parents can have children and must have appropriate members and methods to manage them
    """
    def __init__(self):
        #Private members
        self.__widget_dict=dict()   #Dictionary that stores list of widgets
        self.__widgets_to_render = []   #list of widgets to render


    def add_widget(self, widget):
        """
        The widgets are stored in a list until building of the frame where
        they are procedurally created and bound to the frame
        This method gives public access to add widgets to the list
        """
        # Append to widget list:
        self.__widgets_to_render.append(widget)

    def render_all_widgets(self,master):
        for widget in self.__widgets_to_render:
            self.__render_widget(widget,master)


    def __render_widget(self, widget, master=None):
        """
        Method:
            Builds a widget and binds to frame
        Parameters:
            widget - widget to bind
            master - frame object created during frame's build process
        """

        # Construct widget and bind to frame
        new_widget = widget.build(master)

        # Save the reference to the widget in the widget object
        widget.widget = new_widget

        # Bind events to the widgets event functions
        # This uses Tkinter's bind method which uses a string to identify the action performed on an object
        # The lambda function receives the arguments returned from the event handler and passes it as well
        #   as current object (self) to the event handler function stored.
        # Note that if the event handler variable is empty (None), attempting to pass a variable to a non-existent
        #   function will result in an exception, hence the ternary operator:
        new_widget.bind("<Enter>",
                        lambda args: widget.mouse_over(self, args) if widget.mouse_over is not None else None)
        new_widget.bind("<Leave>",
                        lambda args: widget.mouse_off(self, args) if widget.mouse_off is not None else None)
        new_widget.bind("<Button-1>",
                        lambda args: widget.on_click(self, args) if widget.on_click is not None else None)
        new_widget.bind("<ButtonRelease>",
                        lambda args: widget.on_mouse_up(self, args) if widget.on_mouse_up is not None else None)
        new_widget.bind("<Return>",
                        lambda args: widget.on_return(self, args) if widget.on_return is not None else None)
        new_widget.bind("<Key>",
                        lambda args: widget.on_keypress(self, args) if widget.on_keypress is not None else None)
        new_widget.bind("<KeyRelease>",
                        lambda args: widget.on_keyup(self, args) if widget.on_keyup is not None else None)

        # Pack and Position the new widget:
        new_widget.place(x=widget.left, y=widget.top)

        # Append widget to dictionary
        self.__widget_dict[widget.name] = widget

    def get_context(self,name):
        """
            Method:
                Calls to the object used to create the widget
            Parameters:
                name - Name of object
            Returns:
                Object or None
        """
        # If name exists in dictionary:
        if name in self.__widget_dict:
            # Return dictionary object
            return self.__widget_dict[name]
        else:
            # Else return None
            return None

    def get_child(self, name):
        """
            Method:
                References to the created widgets are stored in a dictionary.
                Widget properties can be accessed by calling the widget from dictionary:
            Parameters:
                name - Name of widget stored in dictionary
            Returns:
                widget object if located else main panel object
        """
        # If name exists in dictionary:
        if name in self.__widget_dict:
            # Return widget
            return self.__widget_dict[name].widget
        else:
            # Else return None
            return None

    def get_text_value(self, name):
        """
            Method:
                Grabs the value stored in the text variable of a textbox object
                Must reference by object name
            Parameters:
                name - Name of widget stored in dictionary
            Returns:
                String value or ""
        """
        if self.get_child(name) is not None and self.get_context(name).type=="text":
            return self.get_child(name).get()
        else:
            return ""

    def set_text_value(self, name, text):
        """
            Method:
                Sets the value stored in the text variable of a textbox object
                Must reference by object name
            Parameters:
                name - Name of widget stored in dictionary
        """
        if self.get_child(name) is not None and self.get_context(name).type=="text":
            tmp = self.get_text_value(name)
            self.get_context(name).text=text
            self.get_child(name).delete(0, len(tmp))
            self.get_child(name).insert(0, text)



class Window(_Parent):
    """
    Window objects are standard GUI windows
    Windows can have widgets attached to them to allow interface
    A list of widgets is kept in the widget dictionary and can be accessed using the widget name
    Text boxes have their text variables stored in a separate dictionary
    """
    #Static constants:
    DEFAULT_FONT_SIZE=20
    DEFAULT_BACKGROUND_COLOR = "gray94"
    DEFAULT_FONT_COLOR = "black"
    StringVar = tk.StringVar  # Call to create a tk str variable type
    IntVar=tk.IntVar    #Call to create a tk int variable type
    DoubleVar=tk.DoubleVar #Call to create a tk double variable type

    #Constructor
    def __init__(self,title,width,height):
        super().__init__()
        #Private Members:
        self.__main_panel=tk.Tk()   #create main window object
        self.__self=self.__main_panel   #A reference to the widget created
        self.__window_title=title   #title displayed in bar
        self.__height=height    #height
        self.__width=width  #width
        self.__widget_dict=dict()   #Dictionary that stores list of widgets
        self.__e_value=dict()   #Special dictionary for text values returned from textboxes
        self.__background = Window.DEFAULT_BACKGROUND_COLOR     #Background color
        self.__forecolor = Window.DEFAULT_FONT_COLOR    #Font color
        #Event handling functions:
        self.__on_click = None
        self.__mouse_over = None
        self.__mouse_off = None
        self.__on_return = None
        self.__on_keypress = None
        self.__on_keyup=None
        self.__on_mouse_up=None




    def display_window(self):
        """
            Method - display_window
                Bind functions and enter into mainloop of window
                Once started, subsequent commands will not run unless bound to an object or window event
        """
        #Bind events to the widgets event functions
        #This uses Tkinter's bind method which uses a string to identify the action performed on an object
        #The lambda function receives the arguments returned from the event handler and passes it as well
        #   as current object (self) to the event handler function stored.
        #Note that if the event handler variable is empty (None), attempting to pass a variable to a non-existent
        #   function will result in an exception, hence the ternary operator:        self.__main_panel.bind("<Enter>", lambda args:self.__mouse_over(self,args) if self.__mouse_over is not None else None)
        self.__main_panel.bind("<Leave>", lambda args:self.__mouse_off(self,args)if self.__mouse_off is not None else None)
        self.__main_panel.bind("<Button-1>", lambda args:self.__on_click(self,args)if self.__on_click is not None else None)
        self.__main_panel.bind("<Return>", lambda args:self.__on_return(self,args)if self.__on_return is not None else None)
        self.__main_panel.bind("<Key>", lambda args: self.__on_keypress(self,args)if self.__on_keypress is not None else None)
        self.__main_panel.bind("<KeyRelease>",
                               lambda args: self.__on_keyup(self, args) if self.__on_keyup is not None else None)
        self.__main_panel.bind("<ButtonRelease>",
                               lambda args: self.__on_mouse_up(self, args) if self.__on_mouse_up is not None else None)
        self.__main_panel.title(self.__window_title)
        self.__main_panel.geometry(f"{self.__width}x{self.__height}")
        self.render_all_widgets(self.__self)
        self.__main_panel.mainloop()

    def exit(self):
        """
        Exit main loop
        """
        self.__main_panel.destroy()


    def set_keypress(self, function):
        """
            Method:
                Binds a new function to keypress event handler
            Parameters:
                function - function to execute
        """
        self.__on_keypress=function #Save function
        #Bind function:
        self.__main_panel.bind("<Key>",
                               lambda args: self.__on_keypress(self,args)if self.__on_keypress is not None else None)

    def set_on_click(self, function):
        """
            Method:
                Binds a new function to the on_click event handler
            Parameters:
                function - function to execute
        """
        self.__on_click=function    #save function
        #Bind function:
        self.__main_panel.bind("<Button-1>",
                               lambda args: self.__on_click(self, args) if self.__on_click is not None else None)

    def set_on_mouseover(self, function):
        """
            Method:
                Binds a new function to the on_click event handler
            Parameters:
                function - function to execute
        """
        self.__mouse_over=function    #save function
        #Bind function:
        self.__main_panel.bind("<Enter>",
                               lambda args: self.__mouse_over(self, args) if self.__mouse_over is not None else None)

    #For testing:
    def func(self):
        pass

    #-------------------Element------------------------
    class _Element:
        """
        Element is an abstract class for widget objects. Should not be implemented. Only inherited
        """
        #Constructor:
        def __init__(self,name,left,top,width, height,back_color,fore_color):
            #Members
            self.name=name  #name
            self.left=left  #x position
            self.top=top    #y position
            self.width=width    #width
            self.height=height  #height - Note not all widgets utilize height property
            self.background=back_color  # background color
            self.forecolor=fore_color   # font color
            self.font_name=""   #Font type
            self.font_size=Window.DEFAULT_FONT_SIZE #Font size
            self.text=self.name
            self.widget=None
            #Event handling variables (These will bind to objects)
            self.on_click=None
            self.on_mouse_up=None
            self.mouse_over=None
            self.mouse_off=None
            self.on_return=None
            self.on_keypress=None
            self.on_keyup=None

    #-------------------Frame--------------------------
    class Frame(_Element,_Parent):
        """
        Frames are elements that hold other elements. Child elements are attached to the frame
        Positional properties of child elements are relative to position of the frame
        """
        index=0 #For indexing frame numbers and auto naming
        #Constructor:
        def __init__(self,name="frame"+str(index),width=10,height=10,left=0,top=0):
            Window._Element.__init__(self,name,left,top,width,height,Window.DEFAULT_BACKGROUND_COLOR,Window.DEFAULT_FONT_COLOR)
            _Parent.__init__(self)
            self.type="frame"
            self.index+=1
            # self.__widget_dict = dict()
            self.__e_value = dict()
            # self.__widgets_to_render=[]
            self.__self=self


        def build(self,master):
            """
            Method:
                Builds the frame object and attaches child widgets
            Parameters:
                master - parent to attach frame to
            Returns:
                Tkinter frame widget
            """
            #Create frame:
            frame= tk.Frame(
                master=master,
                name=self.name,
                background=self.background,
                width=self.width,
                height=self.height,
            )
            #Get all child widgets, and attach to frame
            self.render_all_widgets(frame)

            #Store frame widget for future reference
            self.widget=frame

            #Return frame widget
            return frame

    #-------------------Button-------------------------
    class Button(_Element):
        index=0
        def __init__(self,name="button"+str(index),text="Button1",width=6,height=1,left=0,top=0):
            super().__init__(name,left,top,width,height,Window.DEFAULT_BACKGROUND_COLOR,Window.DEFAULT_FONT_COLOR)
            self.type="button"
            self.text=text
            self.index+=1

        def build(self,master):
            return tk.Button(
                master=master,
                name=self.name,
                text=self.text,
                background=self.background,
                foreground=self.forecolor,
                width=self.width,
                height=self.height,
                font=(self.font_name,self.font_size)
            )
    #-------------------TextBox-------------------------
    class TextBox(_Element):
        index = 0
        def __init__(self,name="textBox"+str(index),width=7,height=1,left=0,top=0):
            super().__init__(name, left, top, width,height,"white", Window.DEFAULT_FONT_COLOR)
            self.type="text"
            self.text=tk.StringVar()
            self.width = width
            self.password_char=""
            self.index+=1

        def build(self,master):
            return tk.Entry(
                master=master,
                name=self.name,
                textvariable=self.text,
                background=self.background,
                foreground=self.forecolor,
                width=self.width,
                show=self.password_char,
                font=(self.font_name,self.font_size)
            )
    #-------------------Label-------------------------
    class Label(_Element):
        index=0
        def __init__(self,name="label"+str(index),text="Label1",width=7,height=1,left=0,top=0):
            super().__init__(name, left, top, width,height,Window.DEFAULT_BACKGROUND_COLOR, Window.DEFAULT_FONT_COLOR)
            self.type="label"
            self.text=text
            self.password_char = ""
            self.index+=1

        def build(self,master):
            return tk.Label(
                master=master,
                name=self.name,
                text=self.text,
                background=self.background,
                foreground=self.forecolor,
                height=self.height,
                width=self.width,
                font=(self.font_name,self.font_size)
            )
    # -------------------RadioButton-------------------------
    class RadioButton(_Element):
        index=0
        def __init__(self,name="radio"+str(index),text="Option",width=7,height=1,left=0,top=0):
            super().__init__(name, left, top, width,height,Window.DEFAULT_BACKGROUND_COLOR, Window.DEFAULT_FONT_COLOR)
            self.type="radio"
            self.text=text
            self.variable=tk.StringVar()
            self.value=self.name
            self.index+=1

        def build(self,master):
            return tk.Radiobutton(
                master=master,
                name=self.name,
                text=self.text,
                value=self.value,
                variable=self.variable,
                background=self.background,
                foreground=self.forecolor,
                height=self.height,
                width=self.width,
                font=(self.font_name,self.font_size)
            )
    # -------------------ComboBox-------------------------

    class ComboBox(_Element):
        index = 0

        def __init__(self, name="combobox" + str(index), options:list=["Select"], initial_selection:int=0, width=7, height=1, left=0, top=0):
            super().__init__(name, left, top, width, height, Window.DEFAULT_BACKGROUND_COLOR, Window.DEFAULT_FONT_COLOR)
            self.type = "combobox"
            self.options=options
            self.initial_selection=initial_selection
            self.variable = tk.StringVar()
            self.index += 1

        def build(self, master):
            return ttk.Combobox(
                master=master,
                name=self.name,
                textvariable=self.variable,
                values=self.options,
                background=self.background,
                foreground=self.forecolor,
                height=self.height,
                width=self.width,
                font=(self.font_name, self.font_size),
            )

 # -------------------ComboBox-------------------------

    class CheckBox(_Element):
        index = 0

        def __init__(self, name="checkbox" + str(index),text:str="", initial_selection:int=0, width=7, height=1, left=0, top=0):
            super().__init__(name, left, top, width, height, Window.DEFAULT_BACKGROUND_COLOR, Window.DEFAULT_FONT_COLOR)
            self.type = "checkbox"
            self.options=[]
            self.initial_selection=initial_selection
            self.variable = tk.IntVar()
            self.index += 1
            self.text=text

        def build(self, master):

            return tk.Checkbutton(
                master=master,
                text=self.text,
                variable=self.variable,
                onvalue=1,
                offvalue=0
            )



## For testing:

# from input_validation import *
# def win_keypress(self,key_event):
#     if key_event.keycode==65:
#         print("You pressed the A key")
#
#
# def keypress(self,key_event):
#     print(key_event.keycode)
#
# def simple_function(self, args):
#     # self.set_text_value("txtNum1","Hooray!")
#     x= validate_float(self.get_text_value("txtNum1"))["value"]
#     y = validate_float(self.get_text_value("txtNum2"))["value"]
#     answer=x+y
#     self.get_child("lblAnswer").config(text=answer)
#
#
# def main(): #for testing
#     my_window=Window("This window",800,600)
#     my_frame=Window.Frame("frmMain1",320,320,200,100)
#
#     my_button=Window.Button("btnExecute","Execute",6,1,0,250)
#     my_button.on_click=simple_function
#     my_frame.add_widget(my_button)
#
#     t=Window.TextBox("txtNum1",20,20,0,100)
#     my_frame.add_widget(t)
#     t = Window.TextBox("txtNum2", 20, 20,0, 150)
#     my_frame.add_widget(t)
#
#
#
#     l=Window.Label("lblAnswer","",20,1,0,200)
#     my_frame.add_widget(l)
#     l = Window.Label("lblLabel", "Let's add two numbers!", 20, 1,  0, 50)
#     my_frame.add_widget(l)
#
#     my_window.add_widget(my_frame)
#     my_window.display_window()
#     print("TEXT")
#
#
# if __name__=="__main__":
#     main()