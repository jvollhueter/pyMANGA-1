#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
List containing species specific plant model parameters.
@date: 2018 - Today
@author: jasper.bathmann@ufz.de
"""


def createPlant():
    ini_r_ag = 0.004
    ini_h_ag = 0.004
    ini_r_bg = 0.005
    ini_h_bg = 0.05
    maint_factor = 0.00000000002
    growth_factor = 0.6
    max_h = 1.5
    w_r_ag = 0.25
    w_h_ag = 0.25
    w_r_bg = 0.25
    w_h_bg = 0.25
    sun_c = 2.5e-8

    geometry = {}
    parameter = {}
    geometry["r_ag"] = ini_r_ag
    geometry["h_ag"] = ini_h_ag
    geometry["r_bg"] = ini_r_bg
    geometry["h_bg"] = ini_h_bg
    parameter["maint_factor"] = maint_factor
    parameter["growth_factor"] = growth_factor
    parameter['w_r_ag'] = w_r_ag
    parameter['w_h_ag'] = w_h_ag
    parameter['w_r_bg'] = w_r_bg
    parameter['w_h_bg'] = w_h_bg
    parameter['w_h_bg'] = w_h_bg
    parameter["max_h"] = max_h
    parameter["sun_c"] = sun_c
    return geometry, parameter
