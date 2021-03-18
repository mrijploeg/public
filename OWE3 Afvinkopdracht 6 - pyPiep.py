import mysql.connector
import tkinter

class GUI:
    def __init__(self):
        # Initialize the class.
        self.__tag = ""
        self.__messages = []
        self.__index = 0

        # Initialize the main window.
        self.main_window = tkinter.Tk()
        self.main_window.title("pyPiep")
        self.main_window.geometry("500x250")

        # Add frames to the main window.
        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)

        # Show the frames.
        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()

        # Add labels to the frames.
        self.message_label = tkinter.Entry(
            self.frame1,
            width=68)
        self.filter_label = tkinter.Label(
            self.frame2,
            text="Filter on #:")
        self.tag_label = tkinter.Entry(
            self.frame2,
            text="")

        # Show the labels.
        self.message_label.pack(side="left")
        self.tag_label.pack(side="right")

        # Add a listbox to the main window.
        self.message_listbox = tkinter.Listbox(
            self.frame3,
            selectmode="single",
            width=400)

        # Add items to the listbox.
        for item in self.__messages:
            self.message_listbox.insert(self.__index, item)
            self.__index += 1

        # Show the listbox.
        self.message_listbox.pack(side="left")

        # Add buttons to the main window.
        self.post_button = tkinter.Button(
            self.frame1,
            text="Post message!",
            command=self.post_buttonclick)
        self.refresh_button = tkinter.Button(
            self.frame2,
            text="Refresh...",
            command=self.refresh_buttonclick)

        # Show the buttons.
        self.post_button.pack(side="left")
        self.filter_label.pack(side="right")
        self.refresh_button.pack(side="right")

        # Show the main window.
        self.main_window.mainloop()

    def post_buttonclick(self):
        """ Post the message in the piep-table when the
        button is clicked.

        """
        # Define the variables.
        message = self.message_label.get()

        # Check if a message was written. If so, use a query to insert
        # the message into the piep-table.
        if message != "":
            cursor.execute(
                "insert into piep (bericht, datum, tijd, student_nr) "
                "values ('" + message + "', curdate(), "
                "curtime(), 654574)")
            connection.commit()

    def refresh_buttonclick(self):
        """ Refresh the listbox when the button is clicked.

        """
        # Define the variables.
        tag = self.tag_label.get()
        self.__messages = []

        # Check if a filter is applied. If so, only display the messages
        # that have the tag in it. If not, display all the messages.
        if tag != "":
            cursor.execute(
                "select voornaam, bericht "
                "from piep join student using (student_nr) "
                "where bericht like '%#" + tag + "%' "
                "order by piep_id desc")
            rows = cursor.fetchall()
            for i in range(len(rows)):
                message = (str(rows[i][1]) + " (" +
                           str(rows[i][0]) + ")")
                self.__messages.append(message)
        else:
            cursor.execute(
                "select voornaam, bericht "
                "from piep join student using (student_nr) "
                "order by piep_id desc")
            rows = cursor.fetchall()
            for i in range(len(rows)):
                message = (str(rows[i][1]) + " (" +
                           str(rows[i][0]) + ")")
                self.__messages.append(message)

        # Remove the previous entries from the listbox.
        self.message_listbox.delete(0, "end")

        # Add the new items to the listbox.
        for item in self.__messages:
            self.message_listbox.insert(self.__index, item)
            self.__index += 1

        # Show the listbox.
        self.message_listbox.pack(side="left")


def connect():
    """ Connect to the database.

    :return connection: object - connection to the database
    :return cursor: object - cursor to write queries
    """
    # Establish a connection.
    connection = mysql.connector.connect(
        host="",
        user="",
        password="",
        db="",
        auth_plugin='mysql_native_password')

    # Open a cursor.
    cursor = connection.cursor()

    # Return the connection and cursor.
    return connection, cursor


def disconnect(connection, cursor):
    """ Disconnect from the database.

    :param connection: object - connection to the database
    :param cursor: object - cursor to write queries
    """
    # Close the cursor and disconnect from the database.
    cursor.close()
    connection.close()


if __name__ == '__main__':
    # Connect to the database.
    connection, cursor = connect()

    # Call the GUI.
    GUI()

    # Disconnect from the database.
    disconnect(connection, cursor)
