# pylint: disable=E0012, fixme, invalid-name, no-member

# pylint: disable=R0913, W0613, W0622, E0611, W0603, R0902, R0903, C0301

import sys
import time
from wave import y_numpy
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QTimer

class MyMainWindow(QMainWindow):
    ''' the main window potentially with menus, statusbar, ... '''

    def __init__(self):
        super().__init__()
        self.resize(900, 300)
        self.move(400, 300)
        central_widget = MyCentralWidget(self)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('PyQt widget with matplotlib animation')
        self.statusBar().showMessage('0')


class MyCentralWidget(QWidget):
    ''' everything in the main area of the main window '''

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        # define figure canvas
        self.mpl_widget = MyMplWidget(self.main_window)
        # place the MyMplWidget into a vertical box layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.mpl_widget) # add the figure
        # use the box layout to fill the window
        self.setLayout(vbox)


class MyMplWidget(FigureCanvas):
    ''' both a QWidget and a matplotlib figure '''

    def __init__(self, main_window, figsize=(4, 3), dpi=100):
        self.main_window = main_window
        # create the figure
        self.fig = plt.figure(figsize=figsize, dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # define attributes for drawing the graph
        self.frame_counter = 0
        self.k_1 = 1.0
        self.k_2 = 2.1
        self.omega = 4.0

        self.plot_wave(0, self.k_1, self.k_2, self.omega)
        # set up the timer for the animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timed_action)
        self.dt = 0.010 # duration between plot updates in seconds, updates every 10ms
        self.timer.start(self.dt*1000)
        self.start_time = time.time() # record time at start of animation

    def timed_action(self):
        ''' both a QWidget and a matplotlib figure '''
        # record times for display
        if self.frame_counter == 0:
            self.start_time = time.time()
            t_now = self.start_time
        else:
            t_now = time.time()

        # redraw the changed elements of the figure
        self.update_wave(t_now, self.k_1, self.k_2, self.omega)
        # every update, show frame time and actual time passed
        mes = f'animation time = {self.frame_counter*self.dt:.1f}, actual time = {t_now-self.start_time:.1f}'
        self.main_window.statusBar().showMessage(mes)

        self.frame_counter += 1

    def plot_wave(self, t, k_1, k_2, omega):
        ''' clear figure and plot wave '''
        self.fig.clf()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.x = np.linspace(-5, 5, 301)
        self.ax.set_ylim([-4, 4])
        self.line, = self.ax.plot(self.x, y_numpy(self.x, t, k_1, k_2, omega), 'b')
        # Plot some axis lines to make things clearer
        self.dashed, = self.ax.plot([0, 0], [-4, 4], "k--")
        self.y_0, = self.ax.plot([self.x.min(), self.x.max()], [0, 0], "k-")
        self.draw()

    def update_wave(self, t, k_1, k_2, omega):
        ''' update relevant components of plot plot sin(kx) for -1 < x < 1 when k changes '''
        self.line.set_ydata(y_numpy(self.x, t, k_1, k_2, omega))
        self.ax.draw_artist(self.ax.patch)                              # <-- redraw the plotting area of the axis
        self.ax.draw_artist(self.line)                                  # <-- redraw the plot line
        self.ax.draw_artist(self.dashed)
        self.ax.draw_artist(self.y_0)
        self.fig.canvas.update()                                        # <-- update the figure
        self.fig.canvas.flush_events()                                  # <-- ensure all draw requests are sent out


app = None

def main():
    """Function executed when this file is run directly"""
    global app
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec()

if __name__ == '__main__':
    main()
