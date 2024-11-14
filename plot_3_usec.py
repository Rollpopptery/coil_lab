# plot_3_usec.py
#
# Plotting raw sample signal , samples are at 3uSec from the WombatPI (arduino Minima)
#
#
# Project:  coil_lab
# wombat.net
#
#
#
#
#
# Modified 14-Nov-2024
#
#
#
#-----------------------------------------------------------------------------------------------------------------------

import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout

from PyQt5.QtWidgets import QVBoxLayout, QWidget

import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

import read_wombat


WINDOW_TITLE = "Wombat plot_3_usec.py   Version 1"
EXPECTED_DATA_SIZE = 50


class PlotWindow(QMainWindow):
    """PlotWindow class for displaying real-time plots."""

    # when the 'take reference' button is pressed, this is updated to be the latest scan
    #
    referencePlot = np.arange(EXPECTED_DATA_SIZE)
    diffPlot = referencePlot

    def __init__(self):
        """Initialize PlotWindow."""
        super().__init__()

        self.setWindowTitle(WINDOW_TITLE)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Vertical layout for overall organization
        self.vertical_layout = QVBoxLayout()
        self.central_widget.setLayout(self.vertical_layout)

        # Horizontal layout for top two plots
        self.horizontal_layout = QHBoxLayout()
        self.vertical_layout.addLayout(self.horizontal_layout)

        # Graphics widget for plots
        self.graphics_widget_top = pg.GraphicsLayoutWidget()
        self.graphics_widget_bottom = pg.GraphicsLayoutWidget()

        # Add top graphics widget to horizontal layout
        self.horizontal_layout.addWidget(self.graphics_widget_top)

        # Add bottom graphics widget to vertical layout
        self.vertical_layout.addWidget(self.graphics_widget_bottom)

        # Create three plots
        self.plot1 = self.graphics_widget_top.addPlot(title='Raw Signal')
        self.plot2 = self.graphics_widget_top.addPlot(title='Difference')

        self.plot3 = self.graphics_widget_bottom.addPlot(title='Normalised', rowspan=1, colspan=2)
        # Sample data (replace with your data)
        data = np.random.rand(100, 100)
        # Display heatmap
        #img = pg.ImageItem(data)
        #self.plot3.addItem(img)


        self.plot1.getAxis('bottom').setLabel('uSec')

        # Generate sample data
        self.x = np.arange(EXPECTED_DATA_SIZE)
        self.y1 = np.sin(self.x)
        self.y2 = np.cos(self.x)

        tick_locations = self.x
        tick_labels = [str(i * 3) for i in self.x]
        ticks = [(i, label) for i, label in enumerate(tick_labels)]
        self.plot1.getAxis('bottom').setTicks([ticks])
        self.plot2.getAxis('bottom').setTicks([ticks])
        self.plot3.getAxis('bottom').setTicks([ticks])



        # Plot data
        self.plot1.plot(self.x, self.y1)
        self.plot2.plot(self.x, self.y2)

        # Horizontal layout for buttons
        self.button_layout = QHBoxLayout()
        self.vertical_layout.addLayout(self.button_layout)


        # Button one
        #
        self.button = QPushButton('Take Reference')
        self.button.setStyleSheet("background-color: #FF0000; color: #FFFFFF")  # Red background, white text
        self.button.setFixedSize(100, 30)  # Set fixed size
        self.button.clicked.connect(self.take_ref_clicked)
        self.button_layout.addWidget(self.button)

        # Button two
        #
        self.button2 = QPushButton('Grab Plot')
        self.button2.setStyleSheet("background-color: #22FF22; color: #FFFFFF")  # Green background, white text
        self.button2.setFixedSize(100, 30)  # Set fixed size
        self.button2.clicked.connect(self.grab_plot_clicked)
        self.button_layout.addWidget(self.button2)

        # Button three
        #
        self.button3 = QPushButton('Clear Plot')
        self.button3.setStyleSheet("background-color: #0000FF; color: #FFFFFF")  # Blue background, white text
        self.button3.setFixedSize(100, 30)  # Set fixed size
        self.button3.clicked.connect(self.clear_plot_clicked)
        self.button_layout.addWidget(self.button3)



        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(200)  # Update every 100ms

    def closeEvent(self, event):
        # Code to execute on window close
        print("Window closed")
        read_wombat.close()
        event.accept()  # Accept close event

    def update_plot(self):
        """Update plot data."""
        # Generate new data

        datablock = read_wombat.getData()
        if(len(datablock) == EXPECTED_DATA_SIZE):
            self.y1 = datablock
            # Update plots

            self.x = np.arange(EXPECTED_DATA_SIZE)
            self.plot1.clear()
            self.plot1.plot(self.x, self.y1)

            self.plot2.clear()
            # Plot the difference between the reference scan and the new scan
            self.diffPlot = np.subtract(self.y1, self.referencePlot)
            self.plot2.plot(self.x, self.diffPlot)

            #self.plot3.clear()
            #self.plot3.plot(self.x, diffPlot)


    def take_ref_clicked(self):
        """Handle button click."""
        print("Button clicked")
        self.referencePlot = self.y1



    def clear_plot_clicked(self):
        """Handle button click."""
        print("Button2 clicked")
        self.plot3.clear()

    def grab_plot_clicked(self):
        """Handle button click."""
        print("Button3 clicked")

        # normalise the latest diferrence plot

        minv = self.diffPlot.min()
        maxv = self.diffPlot.max()

        arr_normalized = (self.diffPlot - minv) / (maxv - minv)

        #print(arr_normalized)
        self.plot3.plot(self.x, arr_normalized)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication


    print("Start Wombat Serial port task")
    read_wombat.runSerial(read_wombat.MODE.SCAN_3USEC)


    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()


    sys.exit(app.exec_())