#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SSB Adalm Pluto RX for QO-100
# Author: ra4hgn
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import os



from gnuradio import qtgui

class pluto_rx(gr.top_block, Qt.QWidget):

    def __init__(self, uri='ip:pluto.local'):
        gr.top_block.__init__(self, "SSB Adalm Pluto RX for QO-100", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SSB Adalm Pluto RX for QO-100")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "pluto_rx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.uri = uri

        ##################################################
        # Variables
        ##################################################
        self.volume = volume = 1.5
        self.tuning = tuning = 0
        self.samp_rate = samp_rate = 512000
        self.reverse = reverse = -1
        self.lnb_lo = lnb_lo = 9749972630
        self.decim = decim = 16
        self.center_freq = center_freq = 739750000
        self.bfo = bfo = 1500
        self.audio_rate_0 = audio_rate_0 = 32e3
        self.audio_rate = audio_rate = 32e3

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(0, 3, 50e-3, 1.5, 200)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, "Volume", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._volume_win)
        self._tuning_range = Range(-250000, 250000, 1, 0, 200)
        self._tuning_win = RangeWidget(self._tuning_range, self.set_tuning, "Tuning", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tuning_win)
        # Create the options list
        self._reverse_options = [-1, 1]
        # Create the labels list
        self._reverse_labels = ['USB', 'LSB']
        # Create the combo box
        self._reverse_tool_bar = Qt.QToolBar(self)
        self._reverse_tool_bar.addWidget(Qt.QLabel("Sideband" + ": "))
        self._reverse_combo_box = Qt.QComboBox()
        self._reverse_tool_bar.addWidget(self._reverse_combo_box)
        for _label in self._reverse_labels: self._reverse_combo_box.addItem(_label)
        self._reverse_callback = lambda i: Qt.QMetaObject.invokeMethod(self._reverse_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._reverse_options.index(i)))
        self._reverse_callback(self.reverse)
        self._reverse_combo_box.currentIndexChanged.connect(
            lambda i: self.set_reverse(self._reverse_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._reverse_tool_bar)
        self._bfo_range = Range(0, 3000, 100, 1500, 200)
        self._bfo_win = RangeWidget(self._bfo_range, self.set_bfo, "Fine tuning", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._bfo_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            4096, #fftsize
            window.WIN_HANN, #wintype
            739750000 + lnb_lo, #fc
            samp_rate, #bw
            "", #name
            False, #plotfreq
            True, #plotwaterfall
            False, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(True)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32(uri if uri else iio.get_pluto_uri(), [True, True], 32768)
        self.iio_pluto_source_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0.set_frequency(center_freq)
        self.iio_pluto_source_0.set_samplerate(samp_rate)
        self.iio_pluto_source_0.set_gain_mode(0, 'slow_attack')
        self.iio_pluto_source_0.set_gain(0, 64)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decim, firdes.low_pass(1.0,samp_rate,3000,100), tuning, samp_rate)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_ff(volume)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(reverse)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_0 = audio.sink(32000, '', True)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(audio_rate, analog.GR_SIN_WAVE, bfo, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(audio_rate, analog.GR_COS_WAVE, bfo, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.qtgui_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pluto_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def setStyleSheetFromFile(self, filename):
        try:
            if not os.path.exists(filename):
                filename = os.path.join(
                    gr.prefix(), "share", "gnuradio", "themes", filename)
            with open(filename) as ss:
                self.setStyleSheet(ss.read())
        except Exception as e:
            print(e, file=sys.stderr)

    def get_uri(self):
        return self.uri

    def set_uri(self, uri):
        self.uri = uri

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_2.set_k(self.volume)

    def get_tuning(self):
        return self.tuning

    def set_tuning(self, tuning):
        self.tuning = tuning
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.tuning)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.low_pass(1.0,self.samp_rate,3000,100))
        self.iio_pluto_source_0.set_samplerate(self.samp_rate)
        self.qtgui_sink_x_0.set_frequency_range(739750000 + self.lnb_lo, self.samp_rate)

    def get_reverse(self):
        return self.reverse

    def set_reverse(self, reverse):
        self.reverse = reverse
        self._reverse_callback(self.reverse)
        self.blocks_multiply_const_vxx_1.set_k(self.reverse)

    def get_lnb_lo(self):
        return self.lnb_lo

    def set_lnb_lo(self, lnb_lo):
        self.lnb_lo = lnb_lo
        self.qtgui_sink_x_0.set_frequency_range(739750000 + self.lnb_lo, self.samp_rate)

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.iio_pluto_source_0.set_frequency(self.center_freq)

    def get_bfo(self):
        return self.bfo

    def set_bfo(self, bfo):
        self.bfo = bfo
        self.analog_sig_source_x_0.set_frequency(self.bfo)
        self.analog_sig_source_x_0_0.set_frequency(self.bfo)

    def get_audio_rate_0(self):
        return self.audio_rate_0

    def set_audio_rate_0(self, audio_rate_0):
        self.audio_rate_0 = audio_rate_0

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.audio_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.audio_rate)



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--uri", dest="uri", type=str, default='ip:pluto.local',
        help="Set URI [default=%(default)r]")
    return parser


def main(top_block_cls=pluto_rx, options=None):
    if options is None:
        options = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(uri=options.uri)

    tb.start()

    tb.setStyleSheetFromFile("/usr/share/gnuradio/themes/plain.qss")
    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
