#!/usr/bin/env python
"""    
Event Selection
 
## Inspired from an event selection script for Higgs->invisible   
"""

__author__ = "Tan Yuhang <tanyuhang@ihep.ac.cn>"
__copyright__ = "Copyright (c) Tanyuhang" 
__created__ = "[2018-09-18 ]"

import sys
import os
import math
import ROOT
import numpy as np
from array import array
from progressbar import Bar, Percentage, ProgressBar
import time
from tools import duration, check_outfile_path

class Cutflow(): 
    def __init__(self):
        self.h_evtflw = ROOT.TH1F('hevtflw','eventflow',10,0,10)
        self.h_evtflw.GetXaxis().SetBinLabel(1,'raw')
        self.h_evtflw.GetXaxis().SetBinLabel(2,'N_{#mu^{+}}=1self.N_{#mu^{-}}=1')
        self.h_evtflw.GetXaxis().SetBinLabel(3,'120GeV/c^{2}<M_{Recoil}<150GeV/c^{2}')
        self.h_evtflw.GetXaxis().SetBinLabel(4,'85GeV/c^{2}<M_{#mu^{+}#mu^{-}}<97GeV/c^{2}')
        self.h_evtflw.GetXaxis().SetBinLabel(5,'12GeV/c<P_{t}^{#mu^{+}#mu^{-}}') 
        self.h_evtflw.GetXaxis().SetBinLabel(6,'#phi_{#mu^{+}#mu^{-}}<175')
        self.h_evtflw.GetXaxis().SetBinLabel(7,'102GeV<Visible Energy<107GeV ')
        self.h_evtflw.GetXaxis().SetBinLabel(8,'The ratio of Energy and P<2.4 ')
        self.h_evtflw.GetXaxis().SetBinLabel(9,'The recoil mass of visible - tau information > 230 GeV')
        self.N=[0.,0.,0.,0.,0.,0.,0.,0.,0.]
        #Before cuts histrogram define
        self.h_before_cut_Pt = ROOT.TH1F('before_cut_Pt','before_cut_P_{t}^{#mu^{+}#mu^{-}}',180,0,90)
        self.h_before_cut_vdt = ROOT.TH1F('before_cut_vdt','before_cut_vdt',480,0,300)
        self.h_before_cut_theta = ROOT.TH1F('before_cut_theta','#phi_{#mu^{+}#mu^{-}}',400,0,200)
        self.h_before_cut_vis = ROOT.TH1F('before_cut_vis','before_cut_Visible Energy',500,0,250)
        self.h_before_cut_Mmumu= ROOT.TH1F('before_cut_Mmumu','before_cut_M_{#mu^{+}#mu^{-}}',300,0,150)
        self.h_before_cut_Mrecoil = ROOT.TH1F('before_cut_Mrecoil','before_cut_M_{Recoil}',140,100,170)
        self.h_before_cut_ep = ROOT.TH1F('before_cut_ep','before_cut_ep',300,1,4)

        #After first cut
        self.h_after_first_cut_Pt = ROOT.TH1F('after_first_cut_Pt','after_first_cut_P_{t}^{#mu^{+}#mu^{-}}',180,0,90)
        self.h_after_first_cut_vdt = ROOT.TH1F('after_first_cut_vdt','after_first_cut_vdt',480,0,240)
        self.h_after_first_cut_theta = ROOT.TH1F('after_first_cut_theta','#phi_{#mu^{+}#mu^{-}}',400,0,200)
        self.h_after_first_cut_vis = ROOT.TH1F('after_first_cut_vis','after_first_cut_Visible Energy',500,0,250)
        self.h_after_first_cut_Mmumu= ROOT.TH1F('after_first_cut_Mmumu','after_first_cut_M_{#mu^{+}#mu^{-}}',300,0,150)
        self.h_after_first_cut_Mrecoil = ROOT.TH1F('after_first_cut_Mrecoil','after_first_cut_M_{Recoil}',140,100,170)
        self.h_after_first_cut_ep = ROOT.TH1F('after_first_cut_ep','after_first_cut_ep',300,1,4)

        #After second cut
        self.h_after_second_cut_Pt = ROOT.TH1F('after_second_cut_Pt','after_second_cut_P_{t}^{#mu^{+}#mu^{-}}',180,0,90)
        self.h_after_second_cut_vdt = ROOT.TH1F('after_second_cut_vdt','after_second_cut_vdt',480,0,240)
        self.h_after_second_cut_theta = ROOT.TH1F('after_second_cut_theta','#phi_{#mu^{+}#mu^{-}}',400,0,200)
        self.h_after_second_cut_vis = ROOT.TH1F('after_second_cut_vis','after_second_cut_Visible Energy',500,0,250)
        self.h_after_second_cut_Mmumu= ROOT.TH1F('after_second_cut_Mmumu','after_second_cut_M_{#mu^{+}#mu^{-}}',300,0,150)
        self.h_after_second_cut_Mrecoil = ROOT.TH1F('after_second_cut_Mrecoil','after_second_cut_M_{Recoil}',140,100,170)
        self.h_after_second_cut_ep = ROOT.TH1F('after_second_cut_ep','after_second_cut_ep',300,1,4)

        #After third cut
        self.h_after_third_cut_Pt = ROOT.TH1F('after_third_cut_Pt','after_third_cut_P_{t}^{#mu^{+}#mu^{-}}',180,0,90)
        self.h_after_third_cut_vdt = ROOT.TH1F('after_third_cut_vdt','after_third_cut_vdt',480,0,240)
        self.h_after_third_cut_theta = ROOT.TH1F('after_third_cut_theta','#phi_{#mu^{+}#mu^{-}}',400,0,200)
        self.h_after_third_cut_vis = ROOT.TH1F('after_third_cut_vis','after_third_cut_Visible Energy',500,0,250)
        self.h_after_third_cut_Mmumu= ROOT.TH1F('after_third_cut_Mmumu','after_third_cut_M_{#mu^{+}#mu^{-}}',300,0,150)
        self.h_after_third_cut_Mrecoil = ROOT.TH1F('after_third_cut_Mrecoil','after_third_cut_M_{Recoil}',140,100,170)
        self.h_after_third_cut_ep = ROOT.TH1F('after_third_cut_ep','after_third_cut_ep',300,1,4)

        #After fourth cut
        self.h_after_fourth_cut_Pt = ROOT.TH1F('after_fourth_cut_Pt','after_fourth_cut_P_{t}^{#mu^{+}#mu^{-}}',180,0,90)
        self.h_after_fourth_cut_vdt = ROOT.TH1F('after_fourth_cut_vdt','after_fourth_cut_vdt',480,0,240)
        self.h_after_fourth_cut_theta = ROOT.TH1F('after_fourth_cut_theta','#phi_{#mu^{+}#mu^{-}}',400,0,200)
        self.h_after_fourth_cut_vis = ROOT.TH1F('after_fourth_cut_vis','after_fourth_cut_Visible Energy',500,0,250)
        self.h_after_fourth_cut_Mmumu= ROOT.TH1F('after_fourth_cut_Mmumu','after_fourth_cut_M_{#mu^{+}#mu^{-}}',300,0,150)
        self.h_after_fourth_cut_Mrecoil = ROOT.TH1F('after_fourth_cut_Mrecoil','after_fourth_cut_M_{Recoil}',140,100,170)
        self.h_after_fourth_cut_ep = ROOT.TH1F('after_fourth_cut_ep','after_fourth_cut_ep',300,1,4)

        #After fifth cut
        self.h_after_fifth_cut_Pt = ROOT.TH1F('after_fifth_cut_Pt','after_fifth_cut_P_{t}^{#mu^{+}#mu^{-}}',180,0,90)
        self.h_after_fifth_cut_vdt = ROOT.TH1F('after_fifth_cut_vdt','after_fifth_cut_vdt',480,0,240)
        self.h_after_fifth_cut_theta = ROOT.TH1F('after_fifth_cut_theta','#phi_{#mu^{+}#mu^{-}}',400,0,200)
        self.h_after_fifth_cut_vis = ROOT.TH1F('after_fifth_cut_vis','after_fifth_cut_Visible Energy',500,0,250)
        self.h_after_fifth_cut_Mmumu= ROOT.TH1F('after_fifth_cut_Mmumu','after_fifth_cut_M_{#mu^{+}#mu^{-}}',300,0,150)
        self.h_after_fifth_cut_Mrecoil = ROOT.TH1F('after_fifth_cut_Mrecoil','after_fifth_cut_M_{Recoil}',140,100,170)
        self.h_after_fifth_cut_ep = ROOT.TH1F('after_fifth_cut_ep','after_fifth_cut_ep',300,1,4)

        #After sixth cut 
        self.h_after_sixth_cut_Pt = ROOT.TH1F('after_sixth_cut_Pt','after_sixth_cut_P_{t}^{#mu^{+}#mu^{-}}',180,0,90)
        self.h_after_sixth_cut_vdt = ROOT.TH1F('after_sixth_cut_vdt','after_sixth_cut_vdt',480,0,240)
        self.h_after_sixth_cut_theta = ROOT.TH1F('after_sixth_cut_theta','#phi_{#mu^{+}#mu^{-}}',400,0,200)
        self.h_after_sixth_cut_vis = ROOT.TH1F('after_sixth_cut_vis','after_sixth_cut_Visible Energy',500,0,250)
        self.h_after_sixth_cut_Mmumu= ROOT.TH1F('after_sixth_cut_Mmumu','after_sixth_cut_M_{#mu^{+}#mu^{-}}',300,0,150)
        self.h_after_sixth_cut_Mrecoil = ROOT.TH1F('after_sixth_cut_Mrecoil','after_sixth_cut_M_{Recoil}',140,100,170)
        self.h_after_sixth_cut_ep = ROOT.TH1F('after_sixth_cut_ep','after_sixth_cut_ep',300,1,4)

        #After seventh cut
        self.h_after_seventh_cut_Pt = ROOT.TH1F('after_seventh_cut_Pt','after_seventh_cut_P_{t}^{#mu^{+}#mu^{-}}',180,0,90)
        self.h_after_seventh_cut_vdt = ROOT.TH1F('after_seventh_cut_vdt','after_seventh_cut_vdt',20,230,240)
        self.h_after_seventh_cut_theta = ROOT.TH1F('after_seventh_cut_theta','#phi_{#mu^{+}#mu^{-}}',400,0,200)
        self.h_after_seventh_cut_vis = ROOT.TH1F('after_seventh_cut_vis','after_seventh_cut_Visible Energy',500,0,250)
        self.h_after_seventh_cut_Mmumu= ROOT.TH1F('after_seventh_cut_Mmumu','after_seventh_cut_M_{#mu^{+}#mu^{-}}',300,0,150)
        self.h_after_seventh_cut_Mrecoil = ROOT.TH1F('after_seventh_cut_Mrecoil','after_seventh_cut_M_{Recoil}',140,100,170)
        self.h_after_seventh_cut_ep = ROOT.TH1F('after_seventh_cut_ep','after_seventh_cut_ep',300,1,4)
        
        #After cut histrogram define
        self.h_after_cut_Pt = ROOT.TH1F('after_cut_Pt','after_cut_P_{t}^{#mu^{+}#mu^{-}}',180,0,90)
        self.h_after_cut_vdt = ROOT.TH1F('after_cut_vdt','after_cut_vdt',140,230,300)
        self.h_after_cut_theta = ROOT.TH1F('after_cut_theta','#phi_{#mu^{+}#mu^{-}}',400,0,200)
        self.h_after_cut_vis = ROOT.TH1F('after_cut_vis','after_cut_Visible Energy',40,90,110)
        self.h_after_cut_Mmumu= ROOT.TH1F('after_cut_Mmumu','after_cut_M_{#mu^{+}#mu^{-}}',40,80,100)
        self.h_after_cut_Mrecoil = ROOT.TH1F('after_cut_Mrecoil','after_cut_M_{Recoil}',40,120,140)
        self.h_after_cut_ep = ROOT.TH1F('after_cut_ep','after_cut_ep',150,1.5,3)

        #Before first cut

        self.m_event=array('i',[0])
        self.m_n_neutral=array('i',[0])
        self.m_Neutral_PID=array('i',[0])	
        self.m_sum_p_neutral=array('f',4*[-99]) 
        self.m_sum_p_photon=array('f',4*[-99])
        self.m_e_photon=array('f',[0])
        self.m_p_leptonp=array('f',4*[-99])
        self.m_p_leptonm=array('f',4*[-99])
        self.m_p_dilepton=array('f',4*[-99])
        self.m_sum_p_charged=array('f',4*[-99])
        self.m_p_Higgsdaughters=array('f',4*[-99])
        self.m_p_Higgsdaughter1=array('f',4*[-99])
        self.m_p_Higgsdaughter2=array('f',4*[-99])
        self.m_p_Zdaughters=array('f',4*[-99])
        self.m_p_Zdaughterp=array('f',4*[-99])
        self.m_p_Zdaughterm=array('f',4*[-99])
        self.m_sum_pt_photon=array('f',[0])
        self.m_pt_dilepton=array('f',[0])
        self.m_pt_leptonm=array('f',[0])
        self.m_pt_leptonp=array('f',[0])
        self.m_e_leptonm=array('f',[0])
        self.m_e_leptonp=array('f',[0])
        self.m_pz_dilepton=array('f',[0])
        self.m_pz_leptonm=array('f',[0])
        self.m_pz_leptonp=array('f',[0])
        self.m_n_charged=array('i',[0])
        self.m_n_gamma=array('i',[0])
        self.m_n_leptonp=array('i',[0])
        self.m_n_leptonm=array('i',[0])
        self.m_n_chargedp=array('i',[0])
        self.m_n_chargedm=array('i',[0])
        self.m_n_Higgsdaughter=array('i',[0])
        self.m_n_neutrino=array('i',[0])
        self.m_m_dimu=array('f',[0])
        self.m_m_recoil=array('f',[0])
        self.m_phi_dilepton_1=array('f',[0])
        self.m_phi_dilepton_2=array('f',[0])
        self.m_cos_miss=array('f',[0])
        self.m_cos_Z=array('f',[0])
        self.m_theta_dilepton=array('f',[0])
        self.m_cos_theta_leptonm=array('f',[0])
        self.m_cos_theta_leptonp=array('f',[0])
        self.m_angle_dilepton=array('f',[0])
        self.m_delta_pt=array('f',[0])
        self.m_energy_neutrino=array('f',[0])
        self.m_p_visible=array('f',4*[-99])
        self.m_energy_visible=array('f',[0])
        self.m_p_visible3=array('f',[0])
        self.m_miss_m=array('f',[0])
        self.m_miss_e=array('f',[0])
        self.m_miss_p=array('f',[0])
        self.m_p_dimu=array('f',[0])
        self.m_p_recoil=array('f',[0])	
        
        self.m_e_other=array('f',[0])
        self.m_m_visible=array('f',[0])
        self.m_e_dimu=array('f',[0])
        self.m_e_recoil=array('f',[0])
        self.m_mine_lepton=array('f',[0])
        self.m_maxe_lepton=array('f',[0])

        self.m_minp_lepton=array('f',4*[-99])
        self.m_maxp_lepton=array('f',4*[-99])

        self.m_e_ep=array('f',[0])
        self.m_l_ep=array('f',[0])

# MC information
        self.m_mc_lepton_minus_id=array('i',[0])
        self.m_mc_lepton_plus_id=array('i',[0])		
        self.m_mc_init_n_lepton_plus=array('i',[0])
        self.m_mc_init_n_lepton_minus=array('i',[0])		
        self.m_mc_init_leptonp_e=array('d',[0])
        self.m_mc_init_leptonp_p=array('d',[0])
        self.m_mc_init_leptonp_pt=array('d',[0])
        self.m_mc_init_leptonp_pz=array('d',[0])
        self.m_mc_init_leptonp_phi=array('d',[0])
        self.m_mc_init_leptonp_theta=array('d',[0])		
        self.m_mc_init_leptonm_e=array('d',[0])
        self.m_mc_init_leptonm_p=array('d',[0])
        self.m_mc_init_leptonm_pt=array('d',[0])
        self.m_mc_init_leptonm_pz=array('d',[0])
        self.m_mc_init_leptonm_phi=array('d',[0])
        self.m_mc_init_leptonm_theta=array('d',[0])		
        self.m_mc_init_dilepton_m=array('d',[0])
        self.m_mc_init_dilepton_e=array('d',[0])
        self.m_mc_init_dilepton_p=array('d',[0])
        self.m_mc_init_dilepton_pt=array('d',[0])
        self.m_mc_init_dilepton_pz=array('d',[0])
        self.m_mc_init_dilepton_rec_m=array('d',[0])
        self.m_mc_init_dilepton_dphi=array('d',[0])
        self.m_mc_init_dilepton_dang=array('d',[0])		
        self.m_mc_init_n_photon=array('i',[0])
        self.m_mc_higgs_m=array('d',[0])
        self.m_mc_higgs_e=array('d',[0])
        self.m_mc_higgs_rec_m=array('d',[0])
        self.m_mc_higgs_decay_type=array('i',[0])		
        self.m_mc_n_Zboson=array('i',[0])		 
        self.m_mc_zw1_m=array('d',[0])
        self.m_mc_zw1_p=array('d',[0])
        self.m_mc_zw1_pt=array('d',[0])
        self.m_mc_zw1_e=array('d',[0])
        self.m_mc_zw1_rec_m=array('d',[0])
        self.m_mc_zw2_m=array('d',[0])
        self.m_mc_zw2_p=array('d',[0])
        self.m_mc_zw2_pt=array('d',[0])
        self.m_mc_zw2_e=array('d',[0])
        self.m_mc_zw2_rec_m=array('d',[0])
        self.m_mc_h2gaugeboson_flag=array('i',[0])  		
        self.m_mc_zw1zw2_m=array('d',[0])
        self.m_mc_zw1zw2_e=array('d',[0])
        self.m_mc_zw1zw2_rec_m=array('d',[0])
        self.m_mc_zz_flag=array('i',[0])
        self.m_mc_ww_flag=array('i',[0])

        self.m_mc_init_photon_e=ROOT.std.vector(float)()
        self.m_mc_init_photon_p=ROOT.std.vector(float)()
        self.m_mc_init_photon_pt=ROOT.std.vector(float)()
        self.m_mc_init_photon_pz=ROOT.std.vector(float)()
        self.m_mc_init_photon_phi=ROOT.std.vector(float)()
        self.m_mc_init_photon_theta=ROOT.std.vector(float)()

        self.m_mc_z1_daughter_pid=ROOT.std.vector(float)()
        self.m_mc_z2_daughter_pid=ROOT.std.vector(float)()
        self.m_mc_pdgid=ROOT.std.vector(float)()
        self.m_mc_init_pdgid=ROOT.std.vector(float)()
        self.m_mc_w1_daughter_pid=ROOT.std.vector(float)()
        self.m_mc_w2_daughter_pid=ROOT.std.vector(float)() 
        self.m_mc_higgs_daughter_pdgid=ROOT.std.vector(float)()


        #tau information 
        self._nTau=array('i',[0])
        self._nTauP=array('i',[0])
        self._nTauM=array('i',[0])
        self._fakeTau=array('i',[0])
        self._totalJet=array('i',[0])

        self._visEp=array('f',[0])
        self._visEm=array('f',[0])

        self._invMp=array('f',[0])
        self._invMm=array('f',[0])

        self._evtN=array('i',[0])
        self._TauTauImpact=array('f',[0])
        self._TauTauD0=array('f',[0])
        self._TauTauZ0=array('f',[0])
        self._tauP_impact=array('f',[0])
        self._tauM_impact=array('f',[0])

        self._RecoilM=array('f',[0])
        self._qqRecoilM=array('f',[0])
        self._TauTauM=array('f',[0])
        self._qqM=array('f',[0])
        self._TotalEvtEn=array('f',[0])

        #tau information 
        self._nTau=array('i',[0])
        self._nTauP=array('i',[0])
        self._nTauM=array('i',[0])
        self._fakeTau=array('i',[0])
        self._totalJet=array('i',[0])

        self._visEp=array('f',[0])
        self._visEm=array('f',[0])

        self._invMp=array('f',[0])
        self._invMm=array('f',[0])

        self._evtN=array('i',[0])
        self._TauTauImpact=array('f',[0])
        self._TauTauD0=array('f',[0])
        self._TauTauZ0=array('f',[0])
        self._tauP_impact=array('f',[0])
        self._tauM_impact=array('f',[0])

        self._RecoilM=array('f',[0])
        self._qqRecoilM=array('f',[0])
        self._TauTauM=array('f',[0])
        self._qqM=array('f',[0])
        self._TotalEvtEn=array('f',[0])


    def plot_before_cut(self,t_in):
        m_pp_lepton=math.sqrt(t_in.m_p_dilepton[0]*t_in.m_p_dilepton[0]+t_in.m_p_dilepton[1]*t_in.m_p_dilepton[1]+t_in.m_p_dilepton[2]*t_in.m_p_dilepton[2])
        m_ee_lepton=t_in.m_p_dilepton[3]
        if m_pp_lepton != 0 and abs(t_in.m_p_dilepton[3])<5000:
            m_l_ep=m_ee_lepton/m_pp_lepton
        else:
            m_l_ep=10
        self.h_before_cut_Pt.Fill(t_in.m_pt_dilepton) 
        self.h_before_cut_vdt.Fill(t_in.TauTauImpact)
        self.h_before_cut_theta.Fill(t_in.m_phi_dilepton_2)
        self.h_before_cut_vis.Fill(t_in.m_energy_visible)
        self.h_before_cut_Mmumu.Fill(t_in.m_m_dimu)
        self.h_before_cut_Mrecoil.Fill(t_in.m_m_recoil)
        self.h_before_cut_ep.Fill(m_l_ep)
    #After first cut
    def plot_after_first_cut(self,t_in,m_l_ep):
    
        self.h_after_first_cut_Pt.Fill(t_in.m_pt_dilepton)
        self.h_after_first_cut_vdt.Fill(t_in.TauTauImpact)
        self.h_after_first_cut_theta.Fill(t_in.m_phi_dilepton_2)
        self.h_after_first_cut_vis.Fill(t_in.m_energy_visible)
        self.h_after_first_cut_Mmumu.Fill(t_in.m_m_dimu)
        self.h_after_first_cut_Mrecoil.Fill(t_in.m_m_recoil)
        self.h_after_first_cut_ep.Fill(m_l_ep) 
    #After second cut
    def plot_after_second_cut(self,t_in,m_l_ep):
    
        self.h_after_second_cut_Pt.Fill(t_in.m_pt_dilepton)
        self.h_after_second_cut_vdt.Fill(t_in.TauTauImpact)
        self.h_after_second_cut_theta.Fill(t_in.m_phi_dilepton_2)
        self.h_after_second_cut_vis.Fill(t_in.m_energy_visible)
        self.h_after_second_cut_Mmumu.Fill(t_in.m_m_dimu)
        self.h_after_second_cut_Mrecoil.Fill(t_in.m_m_recoil)
        self.h_after_second_cut_ep.Fill(m_l_ep)
    #After third cut        
    def plot_after_third_cut(self,t_in,m_l_ep):
    
        self.h_after_third_cut_Pt.Fill(t_in.m_pt_dilepton)
        self.h_after_third_cut_vdt.Fill(t_in.TauTauImpact)
        self.h_after_third_cut_theta.Fill(t_in.m_phi_dilepton_2)
        self.h_after_third_cut_vis.Fill(t_in.m_energy_visible)
        self.h_after_third_cut_Mmumu.Fill(t_in.m_m_dimu)
        self.h_after_third_cut_Mrecoil.Fill(t_in.m_m_recoil)
        self.h_after_third_cut_ep.Fill(m_l_ep) 
    #After fourth cut
    def plot_after_fourth_cut(self,t_in,m_l_ep):
    
        self.h_after_fourth_cut_Pt.Fill(t_in.m_pt_dilepton)
        self.h_after_fourth_cut_vdt.Fill(t_in.TauTauImpact)
        self.h_after_fourth_cut_theta.Fill(t_in.m_phi_dilepton_2)
        self.h_after_fourth_cut_vis.Fill(t_in.m_energy_visible)
        self.h_after_fourth_cut_Mmumu.Fill(t_in.m_m_dimu)
        self.h_after_fourth_cut_Mrecoil.Fill(t_in.m_m_recoil)
        self.h_after_fourth_cut_ep.Fill(m_l_ep)
    #After fifth cut
    def plot_after_fifth_cut(self,t_in,m_l_ep):
    
        self.h_after_fifth_cut_Pt.Fill(t_in.m_pt_dilepton)
        self.h_after_fifth_cut_vdt.Fill(t_in.TauTauImpact)
        self.h_after_fifth_cut_theta.Fill(t_in.m_phi_dilepton_2)
        self.h_after_fifth_cut_vis.Fill(t_in.m_energy_visible)
        self.h_after_fifth_cut_Mmumu.Fill(t_in.m_m_dimu)
        self.h_after_fifth_cut_Mrecoil.Fill(t_in.m_m_recoil)
        self.h_after_fifth_cut_ep.Fill(m_l_ep) 
    #After sixth cut
    def plot_after_sixth_cut(self,t_in,m_l_ep):
    
        self.h_after_sixth_cut_Pt.Fill(t_in.m_pt_dilepton)
        self.h_after_sixth_cut_vdt.Fill(t_in.TauTauImpact)
        self.h_after_sixth_cut_theta.Fill(t_in.m_phi_dilepton_2)
        self.h_after_sixth_cut_vis.Fill(t_in.m_energy_visible)
        self.h_after_sixth_cut_Mmumu.Fill(t_in.m_m_dimu)
        self.h_after_sixth_cut_Mrecoil.Fill(t_in.m_m_recoil)
        self.h_after_sixth_cut_ep.Fill(m_l_ep)  
    #After seventh cut
    def plot_after_seventh_cut(self,t_in,m_l_ep):
    
        self.h_after_seventh_cut_Pt.Fill(t_in.m_pt_dilepton)
        self.h_after_seventh_cut_vdt.Fill(t_in.TauTauImpact)
        self.h_after_seventh_cut_theta.Fill(t_in.m_phi_dilepton_2)
        self.h_after_seventh_cut_vis.Fill(t_in.m_energy_visible)
        self.h_after_seventh_cut_Mmumu.Fill(t_in.m_m_dimu)
        self.h_after_seventh_cut_Mrecoil.Fill(t_in.m_m_recoil)
        self.h_after_seventh_cut_ep.Fill(m_l_ep)

    def plot_after_cut(self,t_in,m_l_ep):

        self.h_after_cut_Pt.Fill(t_in.m_pt_dilepton)
        self.h_after_cut_vdt.Fill(t_in.TauTauImpact)
        self.h_after_cut_theta.Fill(t_in.m_phi_dilepton_2)
        self.h_after_cut_vis.Fill(t_in.m_energy_visible)
        self.h_after_cut_Mmumu.Fill(t_in.m_m_dimu)
        self.h_after_cut_Mrecoil.Fill(t_in.m_m_recoil)
        self.h_after_cut_ep.Fill(m_l_ep)
    def cut(self,t_in,t_out):
        self.N[0]+=1
        self.h_evtflw.Fill(0)
        m_pp_lepton=math.sqrt(t_in.m_p_dilepton[0]*t_in.m_p_dilepton[0]+t_in.m_p_dilepton[1]*t_in.m_p_dilepton[1]+t_in.m_p_dilepton[2]*t_in.m_p_dilepton[2])
        m_ee_lepton=t_in.m_p_dilepton[3]
        if m_pp_lepton != 0 and abs(t_in.m_p_dilepton[3])<5000:
            m_l_ep=m_ee_lepton/m_pp_lepton
        else:
            m_l_ep=10

        if not (t_in.m_n_leptonp==1 and t_in.m_n_leptonm==1):
            return False
        self.N[1]+=1
        self.h_evtflw.Fill(1)
        self.plot_after_first_cut(t_in,m_l_ep)

        if not (t_in.m_m_recoil>120 and t_in.m_m_recoil<150):
            return False
        self.N[2]+=1
        self.h_evtflw.Fill(2)
        self.plot_after_second_cut(t_in,m_l_ep)

        if not (t_in.m_m_dimu>85 and t_in.m_m_dimu<97):
            return False
        self.N[3]+=1
        self.h_evtflw.Fill(3)
        self.plot_after_third_cut(t_in,m_l_ep)

        if not (t_in.m_pt_dilepton>12):
            return False
        self.N[4]+=1
        self.h_evtflw.Fill(4) 
        self.plot_after_fourth_cut(t_in,m_l_ep)

        if not (t_in.m_phi_dilepton_2<175):
            return False
        self.N[5]+=1
        self.h_evtflw.Fill(5)
        self.plot_after_fifth_cut(t_in,m_l_ep)


        if not (t_in.m_energy_visible>102 and t_in.m_energy_visible<107):
            return False
        self.N[6]+=1
        self.h_evtflw.Fill(6)
        self.plot_after_sixth_cut(t_in,m_l_ep)

        if not (m_l_ep<2.4):
            return False  
        self.N[7]+=1
        self.h_evtflw.Fill(7)  
        self.plot_after_seventh_cut(t_in,m_l_ep)       

        if not (t_in.TauTauImpact<0.0007):
            return False

        self.N[8]+=1
        self.h_evtflw.Fill(8)  

        #Plot cuts histrogram after cut
        self.plot_after_cut(t_in,m_l_ep)
#        #Fill root branches after cutting
        self.fill_root(t_in,t_out)

    def fill_root(self,t_in,t_out):

        m_pp_photon=math.sqrt(t_in.m_p_leptonp[0]*t_in.m_p_leptonp[0]+t_in.m_p_leptonp[1]*t_in.m_p_leptonp[1]+t_in.m_p_leptonp[2]*t_in.m_p_leptonp[2])
        m_ee_photon=t_in.m_p_leptonp[3]
        if m_pp_photon != 0 and abs(t_in.m_p_leptonp[3])<5000:
            m_e_ep=m_ee_photon/m_pp_photon
        else:
            m_e_ep=0
        
        m_pp_lepton=math.sqrt(t_in.m_p_dilepton[0]*t_in.m_p_dilepton[0]+t_in.m_p_dilepton[1]*t_in.m_p_dilepton[1]+t_in.m_p_dilepton[2]*t_in.m_p_dilepton[2])
        m_ee_lepton=t_in.m_p_dilepton[3]
        if m_pp_lepton != 0 and abs(t_in.m_p_dilepton[3])<5000:
            m_l_ep=m_ee_lepton/m_pp_lepton
        else:
            m_l_ep=10
            
        LeptonmP = math.sqrt(t_in.m_p_leptonm[0] * t_in.m_p_leptonm[0] +
                             t_in.m_p_leptonm[1] * t_in.m_p_leptonm[1] +
                             t_in.m_p_leptonm[2] * t_in.m_p_leptonm[2])
        LeptonmPz=t_in.m_p_leptonm[2]
        if LeptonmP!=0:
            costheta_leptonm=math.acos(LeptonmPz/LeptonmP)*180/math.pi
        else:
            costheta_leptonm=-999
 
        LeptonpP = math.sqrt(t_in.m_p_leptonp[0] * t_in.m_p_leptonp[0] +
                             t_in.m_p_leptonp[1] * t_in.m_p_leptonp[1] +
                             t_in.m_p_leptonp[2] * t_in.m_p_leptonp[2])
        LeptonpPz=t_in.m_p_leptonp[2]
        if LeptonpPz!=0:
            costheta_leptonp=math.acos(LeptonpPz/LeptonpP)*180/math.pi
        else:
            costheta_leptonp=-999
        self.m_event[0]=t_in.m_event
        self.m_n_neutral[0]=t_in.m_n_neutral
        self.m_Neutral_PID[0]=t_in.m_Neutral_PID
        self.m_e_other[0]=t_in.m_energy_visible-abs(t_in.m_p_leptonm[3])-abs(t_in.m_p_leptonp[3])
        self.m_e_photon[0]=t_in.m_sum_p_photon[3]
        self.m_sum_pt_photon[0]=t_in.m_sum_pt_photon
        self.m_pt_dilepton[0]=t_in.m_pt_dilepton
        self.m_pt_leptonm[0]=math.sqrt(t_in.m_p_leptonm[0]*t_in.m_p_leptonm[0]+t_in.m_p_leptonm[1]*t_in.m_p_leptonm[1])
        self.m_pt_leptonp[0]=math.sqrt(t_in.m_p_leptonp[0]*t_in.m_p_leptonp[0]+t_in.m_p_leptonp[1]*t_in.m_p_leptonp[1])
        self.m_pz_dilepton[0]=t_in.m_p_dilepton[2]
        self.m_pz_leptonm[0]=t_in.m_p_leptonm[2]
        self.m_pz_leptonp[0]=t_in.m_p_leptonp[2]
        self.m_e_leptonm[0]=t_in.m_p_leptonm[3]
        self.m_e_leptonp[0]=t_in.m_p_leptonp[3]
        self.m_n_charged[0]=t_in.m_n_charged
        self.m_n_gamma[0]=t_in.m_n_gamma
        self.m_n_leptonp[0]=t_in.m_n_leptonp
        self.m_n_leptonm[0]=t_in.m_n_leptonm
        self.m_n_chargedp[0]=t_in.m_n_chargedp
        self.m_n_chargedm[0]=t_in.m_n_chargedm
        self.m_n_Higgsdaughter[0]=t_in.m_n_Higgsdaughter
        self.m_n_neutrino[0]=t_in.m_n_neutrino
        self.m_m_dimu[0]=t_in.m_m_dimu
        self.m_m_dimu[0]=math.sqrt(abs(t_in.m_p_dilepton[3]*t_in.m_p_dilepton[3]-t_in.m_p_dilepton[0]*t_in.m_p_dilepton[0]-t_in.m_p_dilepton[1]*t_in.m_p_dilepton[1]-t_in.m_p_dilepton[2]*t_in.m_p_dilepton[2]))
        self.m_m_recoil[0]=t_in.m_m_recoil
        self.m_phi_dilepton_1[0]=t_in.m_phi_dilepton_1
        self.m_phi_dilepton_2[0]=t_in.m_phi_dilepton_2
        self.m_cos_miss[0]=t_in.m_cos_miss
        self.m_cos_Z[0]=t_in.m_cos_Z
        self.m_theta_dilepton[0]=t_in.m_angle_dilepton
        self.m_cos_theta_leptonm[0]=costheta_leptonm
        self.m_cos_theta_leptonp[0]=costheta_leptonp
        self.m_angle_dilepton[0]=t_in.m_angle_dilepton
        self.m_delta_pt[0]=t_in.m_delta_pt
        self.m_energy_neutrino[0]=t_in.m_energy_neutrino
        self.m_miss_m[0]=t_in.m_miss_m
        self.m_miss_e[0]=t_in.m_miss_e
        self.m_energy_visible[0]=t_in.m_energy_visible
        self.m_p_visible3[0]=t_in.m_p_visible[3]
        self.m_m_visible[0]=t_in.m_m_visible
        self.m_e_dimu[0]=t_in.m_e_dimu
        self.m_e_recoil[0]=t_in.m_e_recoil
        self.m_mine_lepton[0]=t_in.m_mine_lepton
        self.m_maxe_lepton[0]=t_in.m_maxe_lepton

        self.m_e_ep[0]=m_e_ep
        self.m_l_ep[0]=m_l_ep	
        self.m_event[0]=t_in.m_event
        self.m_n_neutral[0]=t_in.m_n_neutral
        self.m_Neutral_PID[0]=t_in.m_Neutral_PID
        self.m_e_other[0]=t_in.m_energy_visible-abs(t_in.m_p_leptonm[3])-abs(t_in.m_p_leptonp[3])
        self.m_e_photon[0]=t_in.m_sum_p_photon[3]
        self.m_sum_pt_photon[0]=t_in.m_sum_pt_photon
        self.m_pt_dilepton[0]=t_in.m_pt_dilepton
        self.m_pt_leptonm[0]=math.sqrt(t_in.m_p_leptonm[0]*t_in.m_p_leptonm[0]+t_in.m_p_leptonm[1]*t_in.m_p_leptonm[1])
        self.m_pt_leptonp[0]=math.sqrt(t_in.m_p_leptonp[0]*t_in.m_p_leptonp[0]+t_in.m_p_leptonp[1]*t_in.m_p_leptonp[1])
        self.m_pz_dilepton[0]=t_in.m_p_dilepton[2]
        self.m_pz_leptonm[0]=t_in.m_p_leptonm[2]
        self.m_pz_leptonp[0]=t_in.m_p_leptonp[2]
        self.m_e_leptonm[0]=t_in.m_p_leptonm[3]
        self.m_e_leptonp[0]=t_in.m_p_leptonp[3]
        self.m_n_charged[0]=t_in.m_n_charged
        self.m_n_gamma[0]=t_in.m_n_gamma
        self.m_n_leptonp[0]=t_in.m_n_leptonp
        self.m_n_leptonm[0]=t_in.m_n_leptonm
        self.m_n_chargedp[0]=t_in.m_n_chargedp
        self.m_n_chargedm[0]=t_in.m_n_chargedm
        self.m_n_Higgsdaughter[0]=t_in.m_n_Higgsdaughter
        self.m_n_neutrino[0]=t_in.m_n_neutrino
        self.m_m_dimu[0]=t_in.m_m_dimu
        self.m_m_recoil[0]=t_in.m_m_recoil
        self.m_phi_dilepton_1[0]=t_in.m_phi_dilepton_1
        self.m_phi_dilepton_2[0]=t_in.m_phi_dilepton_2
        self.m_cos_miss[0]=t_in.m_cos_miss
        self.m_cos_Z[0]=t_in.m_cos_Z
        self.m_theta_dilepton[0]=t_in.m_phi_dilepton_2
        self.m_cos_theta_leptonm[0]=costheta_leptonm
        self.m_cos_theta_leptonp[0]=costheta_leptonp
        self.m_angle_dilepton[0]=t_in.m_angle_dilepton
        self.m_delta_pt[0]=t_in.m_delta_pt
        self.m_energy_neutrino[0]=t_in.m_energy_neutrino
        self.m_miss_m[0]=t_in.m_miss_m
        self.m_miss_e[0]=t_in.m_miss_e
        self.m_energy_visible[0]=t_in.m_energy_visible
        self.m_p_visible3[0]=t_in.m_p_visible[3]
        self.m_m_visible[0]=t_in.m_m_visible
        self.m_e_dimu[0]=t_in.m_e_dimu
        self.m_e_recoil[0]=t_in.m_e_recoil
        self.m_p_dimu[0]=t_in.m_p_dimu
        self.m_p_recoil[0]=t_in.m_p_recoil
        self.m_miss_p[0]=t_in.m_miss_p
        self.m_mine_lepton[0]=t_in.m_mine_lepton
        self.m_maxe_lepton[0]=t_in.m_maxe_lepton
        self.m_e_ep[0]=m_e_ep
        self.m_l_ep[0]=m_l_ep
        #MC information

        self.m_mc_lepton_minus_id[0]=t_in.mc_lepton_minus_id
        self.m_mc_lepton_plus_id[0]=t_in.mc_lepton_plus_id	
        self.m_mc_init_n_lepton_plus[0]=t_in.mc_init_n_lepton_plus
        self.m_mc_init_n_lepton_minus[0]=t_in.mc_init_n_lepton_minus		
        self.m_mc_init_leptonp_e[0]=t_in.mc_init_leptonp_e
        self.m_mc_init_leptonp_p[0]=t_in.mc_init_leptonp_p
        self.m_mc_init_leptonp_pt[0]=t_in.mc_init_leptonp_pt
        self.m_mc_init_leptonp_pz[0]=t_in.mc_init_leptonp_pz
        self.m_mc_init_leptonp_phi[0]=t_in.mc_init_leptonp_phi
        self.m_mc_init_leptonp_theta[0]=t_in.mc_init_leptonp_theta	
        self.m_mc_init_leptonm_e[0]=t_in.mc_init_leptonm_e
        self.m_mc_init_leptonm_p[0]=t_in.mc_init_leptonm_p
        self.m_mc_init_leptonm_pt[0]=t_in.mc_init_leptonm_pt
        self.m_mc_init_leptonm_pz[0]=t_in.mc_init_leptonm_pz
        self.m_mc_init_leptonm_phi[0]=t_in.mc_init_leptonm_phi
        self.m_mc_init_leptonm_theta[0]=t_in.mc_init_leptonm_theta	
        self.m_mc_init_dilepton_m[0]=t_in.mc_init_dilepton_m
        self.m_mc_init_dilepton_e[0]=t_in.mc_init_dilepton_e
        self.m_mc_init_dilepton_p[0]=t_in.mc_init_dilepton_p
        self.m_mc_init_dilepton_pt[0]=t_in.mc_init_dilepton_pt
        self.m_mc_init_dilepton_pz[0]=t_in.mc_init_dilepton_pz
        self.m_mc_init_dilepton_rec_m[0]=t_in.mc_init_dilepton_rec_m
        self.m_mc_init_dilepton_dphi[0]=t_in.mc_init_dilepton_dphi
        self.m_mc_init_dilepton_dang[0]=t_in.mc_init_dilepton_dang		
        self.m_mc_init_n_photon[0]=t_in.mc_init_n_photon
        self.m_mc_higgs_m[0]=t_in.mc_higgs_m
        self.m_mc_higgs_e[0]=t_in.mc_higgs_e
        self.m_mc_higgs_rec_m[0]=t_in.mc_higgs_rec_m
        self.m_mc_higgs_decay_type[0]=t_in.mc_higgs_decay_type		
        self.m_mc_n_Zboson[0]=t_in.mc_n_Zboson		
        self.m_mc_zw1_m[0]=t_in.mc_zw1_m
        self.m_mc_zw1_p[0]=t_in.mc_zw1_p
        self.m_mc_zw1_pt[0]=t_in.mc_zw1_pt
        self.m_mc_zw1_e[0]=t_in.mc_zw1_e
        self.m_mc_zw1_rec_m[0]=t_in.mc_zw1_rec_m
        self.m_mc_zw2_m[0]=t_in.mc_zw2_m
        self.m_mc_zw2_p[0]=t_in.mc_zw2_p
        self.m_mc_zw2_pt[0]=t_in.mc_zw2_pt
        self.m_mc_zw2_e[0]=t_in.mc_zw2_e
        self.m_mc_zw2_rec_m[0]=t_in.mc_zw2_rec_m
        self.m_mc_h2gaugeboson_flag[0]=t_in.mc_h2gaugeboson_flag  		
        self.m_mc_zw1zw2_m[0]=t_in.mc_zw1zw2_m
        self.m_mc_zw1zw2_e[0]=t_in.mc_zw1zw2_e
        self.m_mc_zw1zw2_rec_m[0]=t_in.mc_zw1zw2_rec_m
        self.m_mc_zz_flag[0]=t_in.mc_zz_flag
        self.m_mc_ww_flag[0]=t_in.mc_ww_flag 

        #tau information

        self._nTau[0]=t_in.nTau
        self._nTauP[0]=t_in.nTauP
        self._nTauM[0]=t_in.nTauM
        self._fakeTau[0]=t_in.fakeTau
        self._totalJet[0]=t_in.totalJet


        self._visEp[0]=t_in.visEp
        self._visEm[0]=t_in.visEm

        self._invMp[0]=t_in.invMp
        self._invMm[0]=t_in.invMm

        self._evtN[0]=t_in.evtN
        self._TauTauImpact[0]=t_in.TauTauImpact
        self._TauTauD0[0]=t_in.TauTauD0
        self._TauTauZ0[0]=t_in.TauTauZ0
        self._tauP_impact[0]=t_in.tauP_impact
        self._tauM_impact[0]=t_in.tauM_impact

        self._RecoilM[0]=t_in.RecoilM
        self._qqRecoilM[0]=t_in.qqRecoilM
        self._TauTauM[0]=t_in.TauTauM
        self._qqM[0]=t_in.qqM
        self._TotalEvtEn[0]=t_in.TotalEvtEn


        for i in xrange(4):
            self.m_p_visible[i]=t_in.m_p_visible[i]
            self.m_sum_p_photon[i]=t_in.m_sum_p_photon[i]
            self.m_sum_p_neutral[i]=t_in.m_sum_p_neutral[i]
            self.m_p_leptonp[i]=t_in.m_p_leptonp[i]
            self.m_p_leptonm[i]=t_in.m_p_leptonm[i]
            self.m_p_dilepton[i]=t_in.m_p_dilepton[i]
            self.m_sum_p_charged[i]=t_in.m_sum_p_charged[i]
            self.m_p_Higgsdaughters[i]=t_in.m_p_Higgsdaughters[i]
            self.m_p_Higgsdaughter1[i]=t_in.m_p_Higgsdaughter1[i]
            self.m_p_Higgsdaughter2[i]=t_in.m_p_Higgsdaughter2[i]
            self.m_p_Zdaughters[i]=t_in.m_p_Zdaughters[i]
            self.m_p_Zdaughterp[i]=t_in.m_p_Zdaughterp[i]
            self.m_p_Zdaughterm[i]=t_in.m_p_Zdaughterm[i]
            self.m_minp_lepton[i]=t_in.m_minp_lepton[i]
            self.m_maxp_lepton[i]=t_in.m_maxp_lepton[i]
        #MC information
        for i in xrange(len(t_in.mc_init_photon_e)):
    
            self.m_mc_init_photon_e.push_back(t_in.mc_init_photon_e.at(i))
            self.m_mc_init_photon_p.push_back(t_in.mc_init_photon_p.at(i))
            self.m_mc_init_photon_pt.push_back(t_in.mc_init_photon_pt.at(i))
            self.m_mc_init_photon_pz.push_back(t_in.mc_init_photon_pz.at(i))
            self.m_mc_init_photon_phi.push_back(t_in.mc_init_photon_phi.at(i))
            self.m_mc_init_photon_theta.push_back(t_in.mc_init_photon_theta.at(i))  

        for i in xrange (len(t_in.mc_z1_daughter_pid)): 
            self.m_mc_z1_daughter_pid.push_back(t_in.mc_init_photon_theta.at(i))           
        for i in xrange (len(t_in.mc_z2_daughter_pid)):
            self.m_mc_z2_daughter_pid.push_back(t_in.mc_z2_daughter_pid.at(i))           
        for i in xrange (len(t_in.mc_pdgid)):
            if t_in.mc_pdgid[i] < 100:
                self.m_mc_pdgid.push_back(t_in.mc_pdgid.at(i))         
        for i in xrange (len(t_in.mc_init_pdgid)):
            self.m_mc_init_pdgid.push_back(t_in.mc_init_pdgid.at(i))          
        for i in xrange (len(t_in.mc_w1_daughter_pid)):
            self.m_mc_w1_daughter_pid.push_back(t_in.mc_w1_daughter_pid.at(i))           
        for i in xrange (len(t_in.mc_w2_daughter_pid)):
            self.m_mc_w2_daughter_pid.push_back(t_in.mc_w2_daughter_pid.at(i))          
        for i in xrange (len(t_in.mc_higgs_daughter_pdgid)):
            self.m_mc_higgs_daughter_pdgid.push_back(t_in.mc_higgs_daughter_pdgid.at(i)) 

        t_out.Fill()

        self.m_mc_init_photon_e.clear()
        self.m_mc_init_photon_p.clear()
        self.m_mc_init_photon_pt.clear()
        self.m_mc_init_photon_pz.clear()
        self.m_mc_init_photon_phi.clear()
        self.m_mc_init_photon_theta.clear()

        self.m_mc_z1_daughter_pid.clear()
        self.m_mc_z2_daughter_pid.clear()
        self.m_mc_pdgid.clear()
        self.m_mc_init_pdgid.clear()
        self.m_mc_w1_daughter_pid.clear()
        self.m_mc_w2_daughter_pid.clear()
        self.m_mc_higgs_daughter_pdgid.clear()


    def cut_his_write(self):
        self.h_evtflw.Write()
        #before cut
        self.h_before_cut_Pt.Write()
        self.h_before_cut_vdt.Write()
        self.h_before_cut_theta.Write()
        self.h_before_cut_vis.Write()
        self.h_before_cut_Mmumu.Write()
        self.h_before_cut_Mrecoil.Write()
        self.h_before_cut_ep.Write()

# After first cut
        self.h_after_first_cut_Pt.Write()
        self.h_after_first_cut_vdt.Write()
        self.h_after_first_cut_theta.Write()
        self.h_after_first_cut_vis.Write()
        self.h_after_first_cut_Mmumu.Write()
        self.h_after_first_cut_Mrecoil.Write()
        self.h_after_first_cut_ep.Write()
# After second cut
        self.h_after_second_cut_Pt.Write()
        self.h_after_second_cut_vdt.Write()
        self.h_after_second_cut_theta.Write()
        self.h_after_second_cut_vis.Write()
        self.h_after_second_cut_Mmumu.Write()
        self.h_after_second_cut_Mrecoil.Write()
        self.h_after_second_cut_ep.Write()
# After third cut
        self.h_after_third_cut_Pt.Write()
        self.h_after_third_cut_vdt.Write()
        self.h_after_third_cut_theta.Write()
        self.h_after_third_cut_vis.Write()
        self.h_after_third_cut_Mmumu.Write()
        self.h_after_third_cut_Mrecoil.Write()
        self.h_after_third_cut_ep.Write()
# After fourth cut
        self.h_after_fourth_cut_Pt.Write()
        self.h_after_fourth_cut_vdt.Write()
        self.h_after_fourth_cut_theta.Write()
        self.h_after_fourth_cut_vis.Write()
        self.h_after_fourth_cut_Mmumu.Write()
        self.h_after_fourth_cut_Mrecoil.Write()
        self.h_after_fourth_cut_ep.Write()
# After fifth cut

        self.h_after_fifth_cut_Pt.Write()
        self.h_after_fifth_cut_vdt.Write()
        self.h_after_fifth_cut_theta.Write()
        self.h_after_fifth_cut_vis.Write()
        self.h_after_fifth_cut_Mmumu.Write()
        self.h_after_fifth_cut_Mrecoil.Write()
        self.h_after_fifth_cut_ep.Write()
# After sixth cut
        self.h_after_sixth_cut_Pt.Write()
        self.h_after_sixth_cut_vdt.Write()
        self.h_after_sixth_cut_theta.Write()
        self.h_after_sixth_cut_vis.Write()
        self.h_after_sixth_cut_Mmumu.Write()
        self.h_after_sixth_cut_Mrecoil.Write()
        self.h_after_sixth_cut_ep.Write()
# After seventh cut
        self.h_after_seventh_cut_Pt.Write()
        self.h_after_seventh_cut_vdt.Write()
        self.h_after_seventh_cut_theta.Write()
        self.h_after_seventh_cut_vis.Write()
        self.h_after_seventh_cut_Mmumu.Write()
        self.h_after_seventh_cut_Mrecoil.Write()
        self.h_after_seventh_cut_ep.Write()

        #after all cut
        self.h_after_cut_Pt.Write()
        self.h_after_cut_vdt.Write()
        self.h_after_cut_theta.Write()
        self.h_after_cut_vis.Write()
        self.h_after_cut_Mmumu.Write()
        self.h_after_cut_Mrecoil.Write()
        self.h_after_cut_ep.Write()

    def run(self):
        args=sys.argv[1:]
        if len(args)<2:
            print('Input is wrong')
            sys.exit()

        infile=args[0]
        outfile=args[1]

        tmp_file = ROOT.TFile(infile)
        t_in = tmp_file.Get('tree')
        tmp_entries = t_in.GetEntriesFast()

        fout=ROOT.TFile(outfile,"RECREATE")
        t_out=ROOT.TTree('tree','tree')

        t_out.Branch('m_event',self.m_event,'m_event/I')
        t_out.Branch('m_n_neutral',self.m_n_neutral,'m_n_neutral/I')
        t_out.Branch('m_Neutral_PID',self.m_Neutral_PID,'m_Neutral_PID/I')
        t_out.Branch('m_sum_p_neutral',self.m_sum_p_neutral,'m_sum_p_neutral[4]/F')
        t_out.Branch('m_sum_p_photon',self.m_sum_p_photon,'m_sum_p_photon[4]/F')
        t_out.Branch('m_e_photon',self.m_e_photon,'m_e_photon/F')
        t_out.Branch('m_e_other',self.m_e_other,'m_e_other/F')		
        t_out.Branch('m_p_leptonp',self.m_p_leptonp,'m_p_leptonp[4]/F')
        t_out.Branch('m_p_leptonm',self.m_p_leptonm,'m_p_leptonm[4]/F')
        t_out.Branch('m_p_dilepton',self.m_p_dilepton,'m_p_dilepton[4]/F')
        t_out.Branch('m_sum_p_charged',self.m_sum_p_charged,'m_sum_p_charged[4]/F')
        t_out.Branch('m_p_Higgsdaughters',self.m_p_Higgsdaughters,'m_p_Higgsdaughters[4]/F')
        t_out.Branch('m_p_Higgsdaughter1',self.m_p_Higgsdaughter1,'m_p_Higgsdaughter1[4]/F')
        t_out.Branch('m_p_Higgsdaughter2',self.m_p_Higgsdaughter2,'m_p_Higgsdaughter2[4]/F')
        t_out.Branch('m_p_Zdaughters',self.m_p_Zdaughters,'m_p_Zdaughters[4]/F')
        t_out.Branch('m_p_Zdaughterp',self.m_p_Zdaughterp,'m_p_Zdaughterp[4]/F')
        t_out.Branch('m_p_Zdaughterm',self.m_p_Zdaughterm,'m_p_Zdaughterm[4]/F')
        t_out.Branch('m_sum_pt_photon',self.m_sum_pt_photon,'m_sum_pt_photon/F')
        t_out.Branch('m_pt_dilepton',self.m_pt_dilepton,'m_pt_dilepton/F')
        t_out.Branch('m_pt_leptonm',self.m_pt_leptonm,'m_pt_leptonm/F')
        t_out.Branch('m_pt_leptonp',self.m_pt_leptonp,'m_pt_leptonp/F')
        t_out.Branch('m_pz_dilepton',self.m_pz_dilepton,'m_pz_dilepton/F')
        t_out.Branch('m_pz_leptonm',self.m_pz_leptonm,'m_pz_leptonm/F')
        t_out.Branch('m_pz_leptonp',self.m_pz_leptonp,'m_pz_leptonp/F')
        t_out.Branch('m_e_leptonm',self.m_e_leptonm,'m_e_leptonm/F')
        t_out.Branch('m_e_leptonp',self.m_e_leptonp,'m_e_leptonp/F')
        t_out.Branch('m_n_charged',self.m_n_charged,'m_n_charged/I')
        t_out.Branch('m_n_gamma',self.m_n_gamma,'m_n_gamma/I')
        t_out.Branch('m_n_leptonp',self.m_n_leptonp,'m_n_leptonp/I')
        t_out.Branch('m_n_leptonm',self.m_n_leptonm,'m_n_leptonm/I')
        t_out.Branch('m_n_chargedp',self.m_n_chargedp,'m_n_chargedp/I')
        t_out.Branch('m_n_chargedm',self.m_n_chargedm,'m_n_chargedm/I')
        t_out.Branch('m_n_Higgsdaughter',self.m_n_Higgsdaughter,'m_n_Higgsdaughter/I')
        t_out.Branch('m_n_neutrino',self.m_n_neutrino,'m_n_neutrino/I')
        t_out.Branch('m_m_dimu',self.m_m_dimu,'m_m_dimu/F')
        t_out.Branch('m_m_recoil',self.m_m_recoil,'m_m_recoil/F')
        t_out.Branch('m_phi_dilepton_1',self.m_phi_dilepton_1,'m_phi_dilepton_1/F')
        t_out.Branch('m_phi_dilepton_2',self.m_phi_dilepton_2,'m_phi_dilepton_2/F')
        t_out.Branch('m_cos_miss',self.m_cos_miss,'m_cos_miss/F')
        t_out.Branch('m_cos_Z',self.m_cos_Z,'m_cos_Z/F')
        t_out.Branch('m_theta_dilepton',self.m_theta_dilepton,'m_theta_dilepton/F')
        t_out.Branch('m_cos_theta_leptonm',self.m_cos_theta_leptonm,'m_cos_theta_leptonm/F')
        t_out.Branch('m_cos_theta_leptonp',self.m_cos_theta_leptonp,'m_cos_theta_leptonp/F')
        t_out.Branch('m_angle_dilepton',self.m_angle_dilepton,'m_angle_dilepton/F')
        t_out.Branch('m_delta_pt',self.m_delta_pt,'m_delta_pt/F')
        t_out.Branch('m_energy_neutrino',self.m_energy_neutrino,'m_energy_neutrino/F')
        t_out.Branch('m_p_visible',self.m_p_visible,'m_p_visible[4]/F')
        t_out.Branch('m_p_visible3',self.m_p_visible3,'m_p_visible3/F')
        t_out.Branch('m_energy_visible',self.m_energy_visible,'m_energy_visible/F')
        t_out.Branch('m_miss_m',self.m_miss_m,'m_miss_m/F')
        t_out.Branch('m_miss_e',self.m_miss_e,'m_miss_e/F')
        t_out.Branch('m_m_visible',self.m_m_visible,'m_m_visible/F')  
        t_out.Branch('m_e_dimu',self.m_e_dimu,'m_e_dimu/F')
        t_out.Branch('m_e_recoil',self.m_e_recoil,'m_e_recoil/F') 
        t_out.Branch('m_miss_p',self.m_miss_p,'m_miss_p/F')		
        t_out.Branch('m_p_dimu',self.m_p_dimu,'m_p_dimu/F')		
        t_out.Branch('m_p_recoil',self.m_p_recoil,'m_p_recoil/F')

        t_out.Branch("m_mine_lepton",  self.m_mine_lepton,  "m_mine_lepton/F");
        t_out.Branch("m_maxe_lepton",  self.m_maxe_lepton,  "m_maxe_lepton/F");


        t_out.Branch("m_minp_lepton",  self.m_minp_lepton,  "m_minp_lepton[4]/F");
        t_out.Branch("m_maxp_lepton",  self.m_maxp_lepton,  "m_maxp_lepton[4]/F");
        t_out.Branch("m_e_ep",  self.m_e_ep,  "m_e_ep/F");
        t_out.Branch("m_l_ep",  self.m_l_ep,  "m_l_ep/F");

        
        #MC information
        t_out.Branch("mc_pdgid", self.m_mc_pdgid)
        t_out.Branch("mc_init_pdgid", self.m_mc_init_pdgid)
        
        t_out.Branch("mc_lepton_minus_id", self.m_mc_lepton_minus_id, "mc_lepton_minus_id/I")
        t_out.Branch("mc_lepton_plus_id", self.m_mc_lepton_plus_id, "mc_lepton_plus_id/I")
        
        t_out.Branch("mc_init_n_lepton_plus", self.m_mc_init_n_lepton_plus,  "mc_init_n_lepton_plus/I")
        t_out.Branch("mc_init_n_lepton_minus", self.m_mc_init_n_lepton_minus,  "mc_init_n_lepton_minus/I")
        
        t_out.Branch("mc_init_leptonp_e",  self.m_mc_init_leptonp_e,   "mc_init_leptonp_e/D")
        t_out.Branch("mc_init_leptonp_p",  self.m_mc_init_leptonp_p,   "mc_init_leptonp_p/D")
        t_out.Branch("mc_init_leptonp_pt", self.m_mc_init_leptonp_pt,  "mc_init_leptonp_pt/D")
        t_out.Branch("mc_init_leptonp_pz", self.m_mc_init_leptonp_pz,  "mc_init_leptonp_pz/D")

        t_out.Branch("mc_init_leptonp_phi", self.m_mc_init_leptonp_phi,  "mc_init_leptonp_phi/D")
        t_out.Branch("mc_init_leptonp_theta", self.m_mc_init_leptonp_theta,  "mc_init_leptonp_theta/D")
        
        t_out.Branch("mc_init_leptonm_e",  self.m_mc_init_leptonm_e,   "mc_init_leptonm_e/D")
        t_out.Branch("mc_init_leptonm_p",  self.m_mc_init_leptonm_p,   "mc_init_leptonm_p/D")
        t_out.Branch("mc_init_leptonm_pt", self.m_mc_init_leptonm_pt,  "mc_init_leptonm_pt/D")
        t_out.Branch("mc_init_leptonm_pz", self.m_mc_init_leptonm_pz,  "mc_init_leptonm_pz/D")

        t_out.Branch("mc_init_leptonm_phi", self.m_mc_init_leptonm_phi,  "mc_init_leptonm_phi/D")
        t_out.Branch("mc_init_leptonm_theta", self.m_mc_init_leptonm_theta,  "mc_init_leptonm_theta/D")
        
        t_out.Branch("mc_init_dilepton_m",  self.m_mc_init_dilepton_m,   "mc_init_dilepton_m/D")
        t_out.Branch("mc_init_dilepton_e",  self.m_mc_init_dilepton_e,   "mc_init_dilepton_e/D")
        t_out.Branch("mc_init_dilepton_p",  self.m_mc_init_dilepton_p,   "mc_init_dilepton_p/D")
        t_out.Branch("mc_init_dilepton_pt", self.m_mc_init_dilepton_pt,  "mc_init_dilepton_pt/D")
        t_out.Branch("mc_init_dilepton_pz", self.m_mc_init_dilepton_pz,  "mc_init_dilepton_pz/D")
        t_out.Branch("mc_init_dilepton_rec_m", self.m_mc_init_dilepton_rec_m,  "mc_init_dilepton_rec_m/D")
        t_out.Branch("mc_init_dilepton_dphi", self.m_mc_init_dilepton_dphi,  "mc_init_dilepton_dphi/D")
        t_out.Branch("mc_init_dilepton_dang", self.m_mc_init_dilepton_dang,  "mc_init_dilepton_dang/D")
        
        t_out.Branch("mc_init_n_photon", self.m_mc_init_n_photon,  "mc_init_n_photon/I")
        t_out.Branch("mc_init_photon_e",  self.m_mc_init_photon_e)
        t_out.Branch("mc_init_photon_p",  self.m_mc_init_photon_p)
        t_out.Branch("mc_init_photon_pt",  self.m_mc_init_photon_pt)
        t_out.Branch("mc_init_photon_pz",  self.m_mc_init_photon_pz)
        t_out.Branch("mc_init_photon_phi",  self.m_mc_init_photon_phi)
        t_out.Branch("mc_init_photon_theta",  self.m_mc_init_photon_theta)

        t_out.Branch("mc_higgs_m", self.m_mc_higgs_m, "mc_higgs_m/D")
        t_out.Branch("mc_higgs_e", self.m_mc_higgs_e, "mc_higgs_e/D")
        t_out.Branch("mc_higgs_rec_m", self.m_mc_higgs_rec_m, "mc_higgs_rec_m/D")
        t_out.Branch("mc_higgs_decay_type", self.m_mc_higgs_decay_type, "mc_higgs_decay_type/I")
        t_out.Branch("mc_higgs_daughter_pdgid", self.m_mc_higgs_daughter_pdgid)
        
        t_out.Branch("mc_n_Zboson", self.m_mc_n_Zboson, "mc_n_Zboson/I")
        
        t_out.Branch("mc_z1_daughter_pid", self.m_mc_z1_daughter_pid)
        t_out.Branch("mc_z2_daughter_pid", self.m_mc_z2_daughter_pid)

        t_out.Branch("mc_w1_daughter_pid", self.m_mc_w1_daughter_pid)
        t_out.Branch("mc_w2_daughter_pid", self.m_mc_w2_daughter_pid)
        
        t_out.Branch("mc_zw1_m", self.m_mc_zw1_m, "mc_zw1_m/D")
        t_out.Branch("mc_zw1_p", self.m_mc_zw1_p, "mc_zw1_p/D")
        t_out.Branch("mc_zw1_pt", self.m_mc_zw1_pt, "mc_zw1_pt/D")
        t_out.Branch("mc_zw1_e", self.m_mc_zw1_e, "mc_zw1_e/D")
        t_out.Branch("mc_zw1_rec_m", self.m_mc_zw1_rec_m, "mc_zw1_rec_m/D")
        
        t_out.Branch("mc_zw2_m", self.m_mc_zw2_m, "mc_zw2_m/D")
        t_out.Branch("mc_zw2_p", self.m_mc_zw2_p, "mc_zw2_p/D")
        t_out.Branch("mc_zw2_pt", self.m_mc_zw2_pt, "mc_zw2_pt/D")
        t_out.Branch("mc_zw2_e", self.m_mc_zw2_e, "mc_zw2_e/D")
        t_out.Branch("mc_zw2_rec_m", self.m_mc_zw2_rec_m, "mc_zw2_rec_m/D")
        
        t_out.Branch("mc_zw1zw2_m", self.m_mc_zw1zw2_m, "mc_zw1zw2_m/D")
        t_out.Branch("mc_zw1zw2_e", self.m_mc_zw1zw2_e, "mc_zw1zw2_e/D")
        t_out.Branch("mc_zw1zw2_rec_m", self.m_mc_zw1zw2_rec_m, "mc_zw1zw2_rec_m/D")
        t_out.Branch("mc_zz_flag", self.m_mc_zz_flag, "mc_zz_flag/I")
        t_out.Branch("mc_ww_flag", self.m_mc_ww_flag, "mc_ww_flag/I")
        t_out.Branch("mc_h2gaugeboson_flag", self.m_mc_h2gaugeboson_flag, "mc_h2gaugeboson_flag/I")

        #tau information 

        t_out.Branch("nTau", 		self._nTau, 	"nTau/I");
        t_out.Branch("nTauP", 		self._nTauP, 	"nTauP/I");
        t_out.Branch("nTauM", 		self._nTauM, 	"nTauM/I");
        t_out.Branch("fakeTau", 		self._fakeTau, 	"fakeTau/I");
        t_out.Branch("totalJet", 		self._totalJet, 	"totalJet/I");

        t_out.Branch("visEp",	self._visEp,		"visEp/F");
        t_out.Branch("visEm",       self._visEm,          "visEm/F");

        t_out.Branch("invMp",	self._invMp,		"invMp/F");
        t_out.Branch("invMm",       self._invMm,          "invMm/F");

        t_out.Branch("evtN",    self._evtN,       "evtN/I");
        t_out.Branch("TauTauImpact", self._TauTauImpact, "TauTauImpact/F");
        t_out.Branch("TauTauD0", self._TauTauD0, "TauTauD0/F");
        t_out.Branch("TauTauZ0", self._TauTauZ0, "TauTauZ0/F");
        t_out.Branch("tauP_impact", self._tauP_impact, "tauP_impact/F");
        t_out.Branch("tauM_impact", self._tauM_impact, "tauM_impact/F");
        t_out.Branch("RecoilM",    self._RecoilM,       "RecoilM/F");
        t_out.Branch("qqRecoilM",    self._qqRecoilM,       "qqRecoilM/F");
        t_out.Branch("TauTauM",    self._TauTauM,       "TauTauM/F");
        t_out.Branch("qqM",    self._qqM,       "qqM/F");
        t_out.Branch("TotalEvtEn",    self._TotalEvtEn,       "TotalEvtEn/F");



        for i in xrange(tmp_entries):
            t_in.GetEntry(i)
            #Plot cuts histrogram before cut
            self.plot_before_cut(t_in)
            #Cut eventflow and fill histrogram
            self.cut(t_in,t_out)
            #record the select efficiency
#            self.out_eff(t_in,self.N,infile)
        #Write cut flow histrogram
        self.cut_his_write()
        t_out.Write()
        fout.Close()

if __name__ == '__main__':
    start_time = time.clock()
    CUTFLOW = Cutflow()
    CUTFLOW.run()
    print "Cut_successful"
    end_time = time.clock()
print('Running time: %s Seconds'%(end_time-start_time))