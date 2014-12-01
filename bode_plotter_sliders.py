"""
author: Madhav Murthy
title: Bode Plotter
date: 3/23/14
This program allows the user to enter coefficients for the numerator
and denominator of a 3rd order transfer funtion H(s) and generates
the magnitude and phase plots for it.

"""

""" Necessary imports for PyQt GUI """
import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *

""" Necessary imports for plotting """
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot
import numpy as np

""" Import for exception handling """
import warnings


""" Main class that creates the bode plotter application """
class ApplicationWindow(QMainWindow):

    """ Constructor """
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Bode Plotter')

        self.create_main_frame()

    """ Create main frame """
    def create_main_frame(self):
        self.main_frame = QWidget()
        self.create_canvas()
        self.create_controls()

        """ Vertical box layout """
        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(self.hbox)
        vbox.addLayout(self.hbox2)
        vbox.setSpacing(5)
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)



    """ Create GUI controls for user """
    def create_controls(self):

        """ Adding sliders for a, b, c, d in an equation of the
            form a*s3 + b*s2 + c*s + d for the numerator of the transfer
            function
        """
        self.num_label = QLabel('Numerator:')
        self.num_label.setMinimumWidth(90)

        self.num_s3 = QSlider(Qt.Horizontal)
        self.num_s3.setMinimumWidth(100)
        self.num_s3.setMinimum(0)
        self.num_s3.setMaximum(100)
        self.num_s3.setValue(1)
        self.num_s3_label = QLabel(str(self.num_s3.value()/10.0)+'s<sup>3</sup> +')
        self.num_s3_label.setMinimumWidth(60)
        self.connect(self.num_s3, SIGNAL('valueChanged(int)'), self.on_plot)

        self.num_s2 = QSlider(Qt.Horizontal)
        self.num_s2.setMinimumWidth(100)
        self.num_s2.setMinimum(0)
        self.num_s2.setMaximum(100)
        self.num_s2.setValue(1)
        self.num_s2_label = QLabel(str(self.num_s2.value()/10.0)+'s<sup>2</sup> +')
        self.num_s2_label.setMinimumWidth(60)
        self.connect(self.num_s2, SIGNAL('valueChanged(int)'), self.on_plot)

        self.num_s = QSlider(Qt.Horizontal)
        self.num_s.setMinimumWidth(100)
        self.num_s.setMinimum(0)
        self.num_s.setMaximum(100)
        self.num_s.setValue(1)
        self.num_s_label = QLabel(str(self.num_s.value()/10.0)+'s +')
        self.num_s_label.setMinimumWidth(50)
        self.connect(self.num_s, SIGNAL('valueChanged(int)'), self.on_plot)

        self.num_c = QSlider(Qt.Horizontal)
        self.num_c.setMinimumWidth(100)
        self.num_c.setMinimum(0)
        self.num_c.setMaximum(100)
        self.num_c.setValue(1)
        self.num_c_label = QLabel(str(self.num_c.value()/10.0))
        self.num_c_label.setMinimumWidth(40)
        self.connect(self.num_c, SIGNAL('valueChanged(int)'), self.on_plot)


        """ Horizontal box layout for numerator components """
        self.hbox = QHBoxLayout()

        for w in [self.num_label, self.num_s3, self.num_s3_label, self.num_s2,
                  self.num_s2_label, self.num_s, self.num_s_label, self.num_c, self.num_c_label]:
            self.hbox.addWidget(w, alignment=Qt.AlignLeft)

        self.hbox.addStretch()
        self.hbox.setSpacing(5)


        self.message = QErrorMessage(self)


        """ Adding sliders for a, b, c, d in an equation of the
            form a*s3 + b*s2 + c*s + d for the denominator of the transfer
            function
        """
        self.den_label = QLabel('Denominator:')
        self.den_label.setMinimumWidth(90)

        self.den_s3 = QSlider(Qt.Horizontal)
        self.den_s3.setMinimumWidth(100)
        self.den_s3.setMinimum(0)
        self.den_s3.setMaximum(100)
        self.den_s3.setValue(1)
        self.den_s3_label = QLabel(str(self.den_s3.value()/10.0)+'s<sup>3</sup> +')
        self.den_s3_label.setMinimumWidth(60)
        self.connect(self.den_s3, SIGNAL('valueChanged(int)'), self.on_plot)

        self.den_s2 = QSlider(Qt.Horizontal)
        self.den_s2.setMinimumWidth(100)
        self.den_s2.setMinimum(0)
        self.den_s2.setMaximum(100)
        self.den_s2.setValue(1)
        self.den_s2_label = QLabel(str(self.den_s2.value()/10.0)+'s<sup>2</sup> +')
        self.den_s2_label.setMinimumWidth(60)
        self.connect(self.den_s2, SIGNAL('valueChanged(int)'), self.on_plot)

        self.den_s = QSlider(Qt.Horizontal)
        self.den_s.setMinimumWidth(100)
        self.den_s.setMinimum(0)
        self.den_s.setMaximum(100)
        self.den_s.setValue(1)
        self.den_s_label = QLabel(str(self.den_s.value()/10.0)+'s +')
        self.den_s_label.setMinimumWidth(50)
        self.connect(self.den_s, SIGNAL('valueChanged(int)'), self.on_plot)

        self.den_c = QSlider(Qt.Horizontal)
        self.den_c.setMinimumWidth(100)
        self.den_c.setMinimum(0)
        self.den_c.setMaximum(100)
        self.den_c.setValue(1)
        self.den_c_label = QLabel(str(self.den_c.value()/10.0))
        self.den_c_label.setMinimumWidth(40)
        self.connect(self.den_c, SIGNAL('valueChanged(int)'), self.on_plot)

        """ Horizontal box layout for denominator components """
        self.hbox2 = QHBoxLayout()

        for w in [self.den_label, self.den_s3, self.den_s3_label, self.den_s2,
                  self.den_s2_label, self.den_s, self.den_s_label, self.den_c, self.den_c_label]:
            self.hbox2.addWidget(w, alignment=Qt.AlignLeft)

        self.hbox2.addStretch()
        self.hbox2.setSpacing(5)



    """ Create canvas for magnitude and phase plots """
    def create_canvas(self):

        """ Font used for labels """
        font = {'family' : 'sans-serif',
        'color'  : 'black',
        'weight' : 'bold',
        'size'   : 9,
        }

        """ Create figure for plots """
        self.fig = Figure((7.7, 7.0), dpi=100)
        self.fig.patch.set_facecolor('white')
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        """ Define plot style and labels """
        self.axes = self.fig.add_subplot(211)
        self.axes.grid(True, which='major', axis='both')
        self.axes.grid(True, which='minor', axis='x')
        self.axes.set_ylabel("Magnitude (dB)", fontdict=font)
        self.axes.axis([0.1, 100, -40, 0])
        self.axes.set_xscale('log')
        self.axes.tick_params(axis='both', labelsize=7)

        self.axes2 = self.fig.add_subplot(212)
        self.axes2.grid(True, which='major', axis='both')
        self.axes2.grid(True, which='minor', axis='x')
        self.axes2.set_xlabel("Frequency (rad/sec)", fontdict=font)
        self.axes2.set_ylabel("Phase", fontdict=font)
        self.axes2.axis([0.1, 100, -100, 0])
        self.axes2.set_xscale('log')
        self.axes2.tick_params(axis='both', labelsize=7)

        pyplot.grid()
        pyplot.gca().xaxis.grid(True, which='minor')
        pyplot.minorticks_on()
        self.fig.subplots_adjust(hspace=0.30)



    """ Plotting function. Called when plot button is pressed. Plots one
        at a time.Shows error messages if a string that is not a number is
        entered or if an invalid value like infinity is generated.
    """
    def on_plot(self):
        warnings.filterwarnings('error')

        """ Calculating coefficient values """
        num_s3 = self.num_s3.value()/10.0
        num_s2 = self.num_s2.value()/10.0
        num_s = self.num_s.value()/10.0
        num_c = self.num_c.value()/10.0

        den_s3 = self.den_s3.value()/10.0
        den_s2 = self.den_s2.value()/10.0
        den_s = self.den_s.value()/10.0
        den_c = self.den_c.value()/10.0

        """ Reassign Label Values """
        self.num_s3_label.setText(str(num_s3)+'s<sup>3</sup> +')
        self.num_s2_label.setText(str(num_s2)+'s<sup>2</sup> +')
        self.num_s_label.setText(str(num_s)+'s +')
        self.num_c_label.setText(str(num_c))

        self.den_s3_label.setText(str(den_s3)+'s<sup>3</sup> +')
        self.den_s2_label.setText(str(den_s2)+'s<sup>2</sup> +')
        self.den_s_label.setText(str(den_s)+'s +')
        self.den_c_label.setText(str(den_c))


        try:
            if(len(self.axes.lines) > 0):
                self.axes.lines.pop(0)
            if(len(self.axes2.lines) > 0):
                self.axes2.lines.pop(0)
            num_array = [num_s3, num_s2, num_s, num_c]
            den_array = [den_s3, den_s2, den_s, den_c]
            self.wvalues = np.arange(0.1, 100.02, 0.02)
            jw = self.wvalues*1.0j
            y = np.polyval(num_array, jw)/np.polyval(den_array, jw)

            """ Magnitude calculation """
            mag = 20*np.log10(abs(y))

            """ Phase calculation and unwrap """
            phasen = np.arctan2(np.imag(y), np.real(y)) * 180/np.pi
            phase = np.unwrap(phasen)


            """ Redraw plot """
            self.axes.axis([0.1, 100, min(mag) - 5, max(mag) + 5])
            self.axes.semilogx(self.wvalues, mag, 'b')
            self.axes2.axis([0.1, 100, min(phase) - 5, max(phase) + 5])
            self.axes2.semilogx(self.wvalues, phase, 'b')
            self.canvas.draw()
        except Warning:
            self.message.showMessage("Invalid value encountered in divide.")


""" Main method called when program is run """
def main():
    app = QApplication(sys.argv)
    form = ApplicationWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

