#!/usr/bin/env python  
"""
Choose Events
"""
__author__='Tanyh <tanyuhang@ihep.ac.cn>'
__copyright__='Copyright (c) Tanyh'
__created__='[2018-10-19]'
 
import sys
import os
import copy
import ROOT
import random
from array import array
#cut flow histrogram
h_evtflw = ROOT.TH1F('hevtflw','eventflow',10,0,10)
h_evtflw.GetXaxis().SetBinLabel(1,'raw')
h_evtflw.GetXaxis().SetBinLabel(2,'N_{#mu^{+}}>=1&&N_{#mu^{-}}>=1')
h_evtflw.GetXaxis().SetBinLabel(3,'120GeV/c^{2}<M_{Recoil}<150GeV/c^{2}')
h_evtflw.GetXaxis().SetBinLabel(4,'85GeV/c^{2}<M_{#mu^{+}#mu^{-}}<97GeV/c^{2}')
h_evtflw.GetXaxis().SetBinLabel(5,'12GeV/c<P_{t}^{#mu^{+}#mu^{-}}')
h_evtflw.GetXaxis().SetBinLabel(6,'#phi_{#mu^{+}#mu^{-}}<175')
h_evtflw.GetXaxis().SetBinLabel(7,'P_{z}<50GeV')
h_evtflw.GetXaxis().SetBinLabel(8,'102GeV<Visible Energy<107GeV ')
h_evtflw.GetXaxis().SetBinLabel(9,'The ratio of Energy and P<2.4 ')

#root information
m_event=array('i',[0])
m_n_neutral=array('i',[0])
m_sum_p_neutral=array('f',4*[-99]) 
m_sum_p_photon=array('f',4*[-99])
m_p_leptonp=array('f',4*[-99])
m_p_leptonm=array('f',4*[-99])
m_p_dilepton=array('f',4*[-99])
m_sum_p_charged=array('f',4*[-99])
m_p_Higgsdaughters=array('f',4*[-99])
m_p_Higgsdaughter1=array('f',4*[-99])
m_p_Higgsdaughter2=array('f',4*[-99])
m_p_Zdaughters=array('f',4*[-99])
m_p_Zdaughterp=array('f',4*[-99])
m_p_Zdaughterm=array('f',4*[-99])
m_sum_pt_photon=array('f',[0])
m_pt_dilepton=array('f',[0])
m_pt_leptonm=array('f',[0])
m_pt_leptonp=array('f',[0])
m_pz_dilepton=array('f',[0])
m_pz_leptonm=array('f',[0])
m_pz_leptonp=array('f',[0])
m_n_charged=array('i',[0])
m_n_gamma=array('i',[0])
m_n_leptonp=array('i',[0])
m_n_leptonm=array('i',[0])
m_n_chargedp=array('i',[0])
m_n_chargedm=array('i',[0])
m_n_Higgsdaughter=array('i',[0])
m_n_neutrino=array('i',[0])
m_m_dimu=array('f',[0])
m_m_recoil=array('f',[0])
m_phi_dilepton_1=array('f',[0])
m_phi_dilepton_2=array('f',[0])
m_cos_miss=array('f',[0])
m_cos_Z=array('f',[0])
m_theta_dilepton=array('f',[0])
m_cos_theta_leptonm=array('f',[0])
m_cos_theta_leptonp=array('f',[0])
m_angle_dilepton=array('f',[0])
m_delta_pt=array('f',[0])
m_energy_neutrino=array('f',[0])
m_p_visible=array('f',4*[-99])
m_energy_visible=array('f',[0])
m_p_visible3=array('f',[0])
m_miss_m=array('f',[0])
m_miss_e=array('f',[0])
m_e_other=array('f',[0])
m_m_visible=array('f',[0])
m_e_dimu=array('f',[0])
m_e_recoil=array('f',[0])
m_mine_lepton=array('f',[0])
m_maxe_lepton=array('f',[0])

m_miss_p=array('f',[0])
m_p_dimu=array('f',[0])
m_p_recoil=array('f',[0])

m_minp_lepton=array('f',4*[-99])
m_maxp_lepton=array('f',4*[-99])
#MC information
m_mc_lepton_minus_id=array('i',[0])
m_mc_lepton_plus_id=array('i',[0])		
m_mc_init_n_lepton_plus=array('i',[0])
m_mc_init_n_lepton_minus=array('i',[0])		
m_mc_init_leptonp_e=array('d',[0])
m_mc_init_leptonp_p=array('d',[0])
m_mc_init_leptonp_pt=array('d',[0])
m_mc_init_leptonp_pz=array('d',[0])
m_mc_init_leptonp_phi=array('d',[0])
m_mc_init_leptonp_theta=array('d',[0])		
m_mc_init_leptonm_e=array('d',[0])
m_mc_init_leptonm_p=array('d',[0])
m_mc_init_leptonm_pt=array('d',[0])
m_mc_init_leptonm_pz=array('d',[0])
m_mc_init_leptonm_phi=array('d',[0])
m_mc_init_leptonm_theta=array('d',[0])		
m_mc_init_dilepton_m=array('d',[0])
m_mc_init_dilepton_e=array('d',[0])
m_mc_init_dilepton_p=array('d',[0])
m_mc_init_dilepton_pt=array('d',[0])
m_mc_init_dilepton_pz=array('d',[0])
m_mc_init_dilepton_rec_m=array('d',[0])
m_mc_init_dilepton_dphi=array('d',[0])
m_mc_init_dilepton_dang=array('d',[0])		
m_mc_init_n_photon=array('i',[0])
m_mc_higgs_m=array('d',[0])
m_mc_higgs_e=array('d',[0])
m_mc_higgs_rec_m=array('d',[0])
m_mc_higgs_decay_type=array('i',[0])		
m_mc_n_Zboson=array('i',[0])		
m_mc_zw1_m=array('d',[0])
m_mc_zw1_p=array('d',[0])
m_mc_zw1_pt=array('d',[0])
m_mc_zw1_e=array('d',[0])
m_mc_zw1_rec_m=array('d',[0])
m_mc_zw2_m=array('d',[0])
m_mc_zw2_p=array('d',[0])
m_mc_zw2_pt=array('d',[0])
m_mc_zw2_e=array('d',[0])
m_mc_zw2_rec_m=array('d',[0])
m_mc_h2gaugeboson_flag=array('i',[0])  		
m_mc_zw1zw2_m=array('d',[0])
m_mc_zw1zw2_e=array('d',[0])
m_mc_zw1zw2_rec_m=array('d',[0])
m_mc_zz_flag=array('i',[0])
m_mc_ww_flag=array('i',[0])

m_mc_init_photon_e=ROOT.std.vector(float)()
m_mc_init_photon_p=ROOT.std.vector(float)()
m_mc_init_photon_pt=ROOT.std.vector(float)()
m_mc_init_photon_pz=ROOT.std.vector(float)()
m_mc_init_photon_phi=ROOT.std.vector(float)()
m_mc_init_photon_theta=ROOT.std.vector(float)()

m_mc_z1_daughter_pid=ROOT.std.vector(float)()
m_mc_z2_daughter_pid=ROOT.std.vector(float)()
m_mc_pdgid=ROOT.std.vector(float)()
m_mc_init_pdgid=ROOT.std.vector(float)() 
m_mc_w1_daughter_pid=ROOT.std.vector(float)()
m_mc_w2_daughter_pid=ROOT.std.vector(float)() 
m_mc_higgs_daughter_pdgid=ROOT.std.vector(float)()

#tau information 
_nTau=array('i',[0])
_nTauP=array('i',[0])
_nTauM=array('i',[0])
_fakeTau=array('i',[0])
_totalJet=array('i',[0])

_visEp=array('f',[0])
_visEm=array('f',[0])

_invMp=array('f',[0])
_invMm=array('f',[0])

_evtN=array('i',[0])
_TauTauImpact=array('f',[0])
_TauTauD0=array('f',[0])
_TauTauZ0=array('f',[0])
_tauP_impact=array('f',[0])
_tauM_impact=array('f',[0])

_RecoilM=array('f',[0])
_qqRecoilM=array('f',[0])
_TauTauM=array('f',[0])
_qqM=array('f',[0])
_TotalEvtEn=array('f',[0])

def main():
    args=sys.argv[1:]
    infile=args[0]
    outfile=args[1]
    processname=args[2]
    print processname
    table_list=args[3]
    sample = ROOT.TFile(infile)
    b = sample.Get('hevtflw')
    event = []
    for i in range(1,10):
        event.append(b.GetBinContent(i))
    weight = get_weight(event,processname,table_list) 
    root_information(infile,outfile,weight,event)
    

def get_weight(event,processname,table_list):
    event_gen=event[0]            
    IntLum=5600
    table = open(table_list , 'r' )
    cross_section=0.
    for s_line in table :
        if not s_line.startswith('#'):
            l = [x.strip() for x in s_line.split(',')] 
            process=l[0]            
            if processname == process:
                cross_section=l[2]
    if processname=="e2E2h_inv":
        ffH_cross=6.77
        br_Hinv=0.5		
        weight=IntLum*ffH_cross*br_Hinv/event_gen
    elif processname=="eeh_inv":
        ffH_cross=7.04 
        br_Hinv=0.5		
        weight=IntLum*ffH_cross*br_Hinv/event_gen
    elif processname=="qqh_inv":
        ffH_cross=136.81
        br_Hinv=0.5		
        weight=IntLum*ffH_cross*br_Hinv/event_gen		
    elif cross_section==0.:
        print "Sample name misses, please check that!"
        sys.exit() 
    else:
        cs = float(cross_section)
        weight=IntLum*cs/event_gen
    print processname,weight
    return weight
def root_information(infile,outfile,weight,event):
    for i in range(0,9):
        for j in xrange (0,int(event[i]*weight)):
            h_evtflw.Fill(i)
    h =[0]*63
    f = ROOT.TFile(infile)

    h[0] = f.Get('before_cut_Pt')
    h[1] = f.Get('before_cut_vdt')
    h[2] = f.Get('before_cut_theta')
    h[3] = f.Get('before_cut_vis')
    h[4] = f.Get('before_cut_Mmumu')
    h[5] = f.Get('before_cut_Mrecoil')
    h[6] = f.Get('before_cut_ep')

    h[7] = f.Get('after_cut_Pt')
    h[8] = f.Get('after_cut_vdt')
    h[9] = f.Get('after_cut_theta')
    h[10] = f.Get('after_cut_vis')
    h[11] = f.Get('after_cut_Mmumu')
    h[12] = f.Get('after_cut_Mrecoil')
    h[13] = f.Get('after_cut_ep')

    h[14] = f.Get('after_first_cut_Pt')
    h[15] = f.Get('after_first_cut_vdt')
    h[16] = f.Get('after_first_cut_theta')
    h[17] = f.Get('after_first_cut_vis')
    h[18] = f.Get('after_first_cut_Mmumu')
    h[19] = f.Get('after_first_cut_Mrecoil')
    h[20] = f.Get('after_first_cut_ep')

    h[21] = f.Get('after_second_cut_Pt')
    h[22] = f.Get('after_second_cut_vdt')
    h[23] = f.Get('after_second_cut_theta')
    h[24] = f.Get('after_second_cut_vis')
    h[25] = f.Get('after_second_cut_Mmumu')
    h[26] = f.Get('after_second_cut_Mrecoil')
    h[27] = f.Get('after_second_cut_ep')

    h[28] = f.Get('after_third_cut_Pt')
    h[29] = f.Get('after_third_cut_vdt')
    h[30] = f.Get('after_third_cut_theta')
    h[31] = f.Get('after_third_cut_vis')
    h[32] = f.Get('after_third_cut_Mmumu')
    h[33] = f.Get('after_third_cut_Mrecoil')
    h[34] = f.Get('after_third_cut_ep')

    h[35] = f.Get('after_fourth_cut_Pt')
    h[36] = f.Get('after_fourth_cut_vdt')
    h[37] = f.Get('after_fourth_cut_theta')
    h[38] = f.Get('after_fourth_cut_vis')
    h[39] = f.Get('after_fourth_cut_Mmumu')
    h[40] = f.Get('after_fourth_cut_Mrecoil')
    h[41] = f.Get('after_fourth_cut_ep')

    h[42] = f.Get('after_fifth_cut_Pt')
    h[43] = f.Get('after_fifth_cut_vdt')
    h[44] = f.Get('after_fifth_cut_theta')
    h[45] = f.Get('after_fifth_cut_vis')
    h[46] = f.Get('after_fifth_cut_Mmumu')
    h[47] = f.Get('after_fifth_cut_Mrecoil')
    h[48] = f.Get('after_fifth_cut_ep')

    h[49] = f.Get('after_sixth_cut_Pt')
    h[50] = f.Get('after_sixth_cut_vdt')
    h[51] = f.Get('after_sixth_cut_theta')
    h[52] = f.Get('after_sixth_cut_vis')
    h[53] = f.Get('after_sixth_cut_Mmumu')
    h[54] = f.Get('after_sixth_cut_Mrecoil')
    h[55] = f.Get('after_sixth_cut_ep')

    h[56] = f.Get('after_seventh_cut_Pt')
    h[57] = f.Get('after_seventh_cut_vdt')
    h[58] = f.Get('after_seventh_cut_theta')
    h[59] = f.Get('after_seventh_cut_vis')
    h[60] = f.Get('after_seventh_cut_Mmumu')
    h[61] = f.Get('after_seventh_cut_Mrecoil')
    h[62] = f.Get('after_seventh_cut_ep')
        
    for i in range(0,63):
        h[i].Scale(weight)

    fin=ROOT.TFile(infile)
    t_in=fin.Get('tree')
    entries=t_in.GetEntriesFast()
    t_in.SetBranchAddress('m_event',m_event)
    t_in.SetBranchAddress('m_sum_p_neutral',m_sum_p_neutral)
    t_in.SetBranchAddress('m_sum_p_photon',m_sum_p_photon)
    t_in.SetBranchAddress('m_p_leptonp',m_p_leptonp)
    t_in.SetBranchAddress('m_p_leptonm',m_p_leptonm)
    t_in.SetBranchAddress('m_p_dilepton',m_p_dilepton)
    t_in.SetBranchAddress('m_sum_p_charged',m_sum_p_charged)
    t_in.SetBranchAddress('m_p_Higgsdaughters',m_p_Higgsdaughters)
    t_in.SetBranchAddress('m_p_Higgsdaughter1',m_p_Higgsdaughter1)
    t_in.SetBranchAddress('m_p_Higgsdaughter2',m_p_Higgsdaughter2)
    t_in.SetBranchAddress('m_p_Zdaughters',m_p_Zdaughters)
    t_in.SetBranchAddress('m_p_Zdaughterp',m_p_Zdaughterp)
    t_in.SetBranchAddress('m_p_Zdaughterm',m_p_Zdaughterm)
    t_in.SetBranchAddress('m_sum_pt_photon',m_sum_pt_photon)
    t_in.SetBranchAddress('m_pt_dilepton',m_pt_dilepton)
    t_in.SetBranchAddress('m_pt_leptonm',m_pt_leptonm)
    t_in.SetBranchAddress('m_pt_leptonp',m_pt_leptonp)
    t_in.SetBranchAddress('m_pz_dilepton',m_pz_dilepton)
    t_in.SetBranchAddress('m_pz_leptonm',m_pz_leptonm)
    t_in.SetBranchAddress('m_pz_leptonp',m_pz_leptonp)
    t_in.SetBranchAddress('m_n_charged',m_n_charged)
    t_in.SetBranchAddress('m_n_gamma',m_n_gamma)
    t_in.SetBranchAddress('m_n_leptonp',m_n_leptonp)
    t_in.SetBranchAddress('m_n_leptonm',m_n_leptonm)
    t_in.SetBranchAddress('m_n_chargedp',m_n_chargedp)
    t_in.SetBranchAddress('m_n_chargedm',m_n_chargedm)
    t_in.SetBranchAddress('m_n_Higgsdaughter',m_n_Higgsdaughter)
    t_in.SetBranchAddress('m_n_neutrino',m_n_neutrino)
    t_in.SetBranchAddress('m_m_dimu',m_m_dimu)
    t_in.SetBranchAddress('m_m_recoil',m_m_recoil)
    t_in.SetBranchAddress('m_phi_dilepton_1',m_phi_dilepton_1)
    t_in.SetBranchAddress('m_phi_dilepton_2',m_phi_dilepton_2)
    t_in.SetBranchAddress('m_cos_miss',m_cos_miss)
    t_in.SetBranchAddress('m_cos_Z',m_cos_Z)
    t_in.SetBranchAddress('m_theta_dilepton',m_theta_dilepton)
    t_in.SetBranchAddress('m_cos_theta_leptonm',m_cos_theta_leptonm)
    t_in.SetBranchAddress('m_cos_theta_leptonp',m_cos_theta_leptonp)
    t_in.SetBranchAddress('m_angle_dilepton',m_angle_dilepton)
    t_in.SetBranchAddress('m_delta_pt',m_delta_pt)
    t_in.SetBranchAddress('m_energy_neutrino',m_energy_neutrino)
    t_in.SetBranchAddress('m_p_visible',m_p_visible)
    t_in.SetBranchAddress('m_p_visible3',m_p_visible3)
    t_in.SetBranchAddress('m_energy_visible',m_energy_visible)
    t_in.SetBranchAddress('m_miss_m',m_miss_m)
    t_in.SetBranchAddress('m_miss_e',m_miss_e)   

    t_in.SetBranchAddress('m_e_other',m_e_other)
    t_in.SetBranchAddress('m_m_visible',m_m_visible)
    t_in.SetBranchAddress('m_e_dimu',m_e_dimu)
    t_in.SetBranchAddress('m_e_recoil',m_e_recoil)
    t_in.SetBranchAddress('m_mine_lepton',m_mine_lepton)
    t_in.SetBranchAddress('m_maxe_lepton',m_maxe_lepton)
    t_in.SetBranchAddress('m_minp_lepton',m_minp_lepton)
    t_in.SetBranchAddress('m_maxp_lepton',m_maxp_lepton)

    t_in.SetBranchAddress('m_miss_p',m_miss_p)
    t_in.SetBranchAddress('m_p_dimu',m_p_dimu)
    t_in.SetBranchAddress('m_p_recoil',m_p_recoil)

    #MC information 
    t_in.SetBranchAddress("mc_pdgid", m_mc_pdgid)
    t_in.SetBranchAddress("mc_init_pdgid", m_mc_init_pdgid)
    
    t_in.SetBranchAddress("mc_lepton_minus_id", m_mc_lepton_minus_id)
    t_in.SetBranchAddress("mc_lepton_plus_id", m_mc_lepton_plus_id)
    
    t_in.SetBranchAddress("mc_init_n_lepton_plus", m_mc_init_n_lepton_plus)
    t_in.SetBranchAddress("mc_init_n_lepton_minus", m_mc_init_n_lepton_minus)
    
    t_in.SetBranchAddress("mc_init_leptonp_e",  m_mc_init_leptonp_e)
    t_in.SetBranchAddress("mc_init_leptonp_p",  m_mc_init_leptonp_p)
    t_in.SetBranchAddress("mc_init_leptonp_pt", m_mc_init_leptonp_pt)
    t_in.SetBranchAddress("mc_init_leptonp_pz", m_mc_init_leptonp_pz)

    t_in.SetBranchAddress("mc_init_leptonp_phi", m_mc_init_leptonp_phi)
    t_in.SetBranchAddress("mc_init_leptonp_theta", m_mc_init_leptonp_theta)
    
    t_in.SetBranchAddress("mc_init_leptonm_e",  m_mc_init_leptonm_e)
    t_in.SetBranchAddress("mc_init_leptonm_p",  m_mc_init_leptonm_p)
    t_in.SetBranchAddress("mc_init_leptonm_pt", m_mc_init_leptonm_pt)
    t_in.SetBranchAddress("mc_init_leptonm_pz", m_mc_init_leptonm_pz)

    t_in.SetBranchAddress("mc_init_leptonm_phi", m_mc_init_leptonm_phi)
    t_in.SetBranchAddress("mc_init_leptonm_theta", m_mc_init_leptonm_theta)
    
    t_in.SetBranchAddress("mc_init_dilepton_m",  m_mc_init_dilepton_m)
    t_in.SetBranchAddress("mc_init_dilepton_e",  m_mc_init_dilepton_e)
    t_in.SetBranchAddress("mc_init_dilepton_p",  m_mc_init_dilepton_p)
    t_in.SetBranchAddress("mc_init_dilepton_pt", m_mc_init_dilepton_pt)
    t_in.SetBranchAddress("mc_init_dilepton_pz", m_mc_init_dilepton_pz)
    t_in.SetBranchAddress("mc_init_dilepton_rec_m", m_mc_init_dilepton_rec_m)
    t_in.SetBranchAddress("mc_init_dilepton_dphi", m_mc_init_dilepton_dphi)
    t_in.SetBranchAddress("mc_init_dilepton_dang", m_mc_init_dilepton_dang)
    
    t_in.SetBranchAddress("mc_init_n_photon", m_mc_init_n_photon)
    t_in.SetBranchAddress("mc_init_photon_e",  m_mc_init_photon_e)
    t_in.SetBranchAddress("mc_init_photon_p",  m_mc_init_photon_p)
    t_in.SetBranchAddress("mc_init_photon_pt",  m_mc_init_photon_pt)
    t_in.SetBranchAddress("mc_init_photon_pz",  m_mc_init_photon_pz)
    t_in.SetBranchAddress("mc_init_photon_phi",  m_mc_init_photon_phi)
    t_in.SetBranchAddress("mc_init_photon_theta",  m_mc_init_photon_theta)

    t_in.SetBranchAddress("mc_higgs_m", m_mc_higgs_m)
    t_in.SetBranchAddress("mc_higgs_e", m_mc_higgs_e)
    t_in.SetBranchAddress("mc_higgs_rec_m", m_mc_higgs_rec_m)
    t_in.SetBranchAddress("mc_higgs_decay_type", m_mc_higgs_decay_type)
    t_in.SetBranchAddress("mc_higgs_daughter_pdgid", m_mc_higgs_daughter_pdgid)
    
    t_in.SetBranchAddress("mc_n_Zboson", m_mc_n_Zboson)
    
    t_in.SetBranchAddress("mc_z1_daughter_pid", m_mc_z1_daughter_pid)
    t_in.SetBranchAddress("mc_z2_daughter_pid", m_mc_z2_daughter_pid)

    t_in.SetBranchAddress("mc_w1_daughter_pid", m_mc_w1_daughter_pid)
    t_in.SetBranchAddress("mc_w2_daughter_pid", m_mc_w2_daughter_pid)
    
    t_in.SetBranchAddress("mc_zw1_m", m_mc_zw1_m)
    t_in.SetBranchAddress("mc_zw1_p", m_mc_zw1_p)
    t_in.SetBranchAddress("mc_zw1_pt", m_mc_zw1_pt)
    t_in.SetBranchAddress("mc_zw1_e", m_mc_zw1_e)
    t_in.SetBranchAddress("mc_zw1_rec_m", m_mc_zw1_rec_m)
    
    t_in.SetBranchAddress("mc_zw2_m", m_mc_zw2_m)
    t_in.SetBranchAddress("mc_zw2_p", m_mc_zw2_p)
    t_in.SetBranchAddress("mc_zw2_pt", m_mc_zw2_pt)
    t_in.SetBranchAddress("mc_zw2_e", m_mc_zw2_e)
    t_in.SetBranchAddress("mc_zw2_rec_m", m_mc_zw2_rec_m)
    
    t_in.SetBranchAddress("mc_zw1zw2_m", m_mc_zw1zw2_m)
    t_in.SetBranchAddress("mc_zw1zw2_e", m_mc_zw1zw2_e)
    t_in.SetBranchAddress("mc_zw1zw2_rec_m", m_mc_zw1zw2_rec_m)
    t_in.SetBranchAddress("mc_zz_flag", m_mc_zz_flag)
    t_in.SetBranchAddress("mc_ww_flag", m_mc_ww_flag)
    t_in.SetBranchAddress("mc_h2gaugeboson_flag", m_mc_h2gaugeboson_flag)
    #tau information
    t_in.SetBranchAddress("nTau", _nTau);
    t_in.SetBranchAddress("nTauP", _nTauP);
    t_in.SetBranchAddress("nTauM", _nTauM);
    t_in.SetBranchAddress("fakeTau", _fakeTau);
    t_in.SetBranchAddress("totalJet", _totalJet);
    t_in.SetBranchAddress("visEp",_visEp);
    t_in.SetBranchAddress("visEm",_visEm);
    t_in.SetBranchAddress("invMp",_invMp);
    t_in.SetBranchAddress("invMm",_invMm);
    t_in.SetBranchAddress("evtN",_evtN);
    t_in.SetBranchAddress("TauTauImpact",_TauTauImpact);
    t_in.SetBranchAddress("TauTauD0",_TauTauD0);
    t_in.SetBranchAddress("TauTauZ0", _TauTauZ0);
    t_in.SetBranchAddress("tauP_impact", _tauP_impact);
    t_in.SetBranchAddress("tauM_impact", _tauM_impact);
    t_in.SetBranchAddress("RecoilM", _RecoilM);
    t_in.SetBranchAddress("qqRecoilM", _qqRecoilM);
    t_in.SetBranchAddress("TauTauM",  _TauTauM);
    t_in.SetBranchAddress("qqM",_qqM);
    t_in.SetBranchAddress("TotalEvtEn",_TotalEvtEn);


    fout=ROOT.TFile(outfile,"RECREATE")
    t_out=ROOT.TTree('tree','tree')

    t_out.Branch('m_event',m_event,'m_event/I')
    t_out.Branch('m_sum_p_neutral',m_sum_p_neutral,'m_sum_p_neutral[4]/F')
    t_out.Branch('m_sum_p_photon',m_sum_p_photon,'m_sum_p_photon[4]/F')
    t_out.Branch('m_p_leptonp',m_p_leptonp,'m_p_leptonp[4]/F')
    t_out.Branch('m_p_leptonm',m_p_leptonm,'m_p_leptonm[4]/F')
    t_out.Branch('m_p_dilepton',m_p_dilepton,'m_p_dilepton[4]/F')
    t_out.Branch('m_sum_p_charged',m_sum_p_charged,'m_sum_p_charged[4]/F')
    t_out.Branch('m_p_Higgsdaughters',m_p_Higgsdaughters,'m_p_Higgsdaughters[4]/F')
    t_out.Branch('m_p_Higgsdaughter1',m_p_Higgsdaughter1,'m_p_Higgsdaughter1[4]/F')
    t_out.Branch('m_p_Higgsdaughter2',m_p_Higgsdaughter2,'m_p_Higgsdaughter2[4]/F')
    t_out.Branch('m_p_Zdaughters',m_p_Zdaughters,'m_p_Zdaughters[4]/F')
    t_out.Branch('m_p_Zdaughterp',m_p_Zdaughterp,'m_p_Zdaughterp[4]/F')
    t_out.Branch('m_p_Zdaughterm',m_p_Zdaughterm,'m_p_Zdaughterm[4]/F')
    t_out.Branch('m_sum_pt_photon',m_sum_pt_photon,'m_sum_pt_photon/F')
    t_out.Branch('m_pt_dilepton',m_pt_dilepton,'m_pt_dilepton/F')
    t_out.Branch('m_pt_leptonm',m_pt_leptonm,'m_pt_leptonm/F')
    t_out.Branch('m_pt_leptonp',m_pt_leptonp,'m_pt_leptonp/F')
    t_out.Branch('m_pz_dilepton',m_pz_dilepton,'m_pz_dilepton/F')
    t_out.Branch('m_pz_leptonm',m_pz_leptonm,'m_pz_leptonm/F')
    t_out.Branch('m_pz_leptonp',m_pz_leptonp,'m_pz_leptonp/F')
    t_out.Branch('m_n_charged',m_n_charged,'m_n_charged/I')
    t_out.Branch('m_n_gamma',m_n_gamma,'m_n_gamma/I')
    t_out.Branch('m_n_leptonp',m_n_leptonp,'m_n_leptonp/I')
    t_out.Branch('m_n_leptonm',m_n_leptonm,'m_n_leptonm/I')
    t_out.Branch('m_n_chargedp',m_n_chargedp,'m_n_chargedp/I')
    t_out.Branch('m_n_chargedm',m_n_chargedm,'m_n_chargedm/I')
    t_out.Branch('m_n_Higgsdaughter',m_n_Higgsdaughter,'m_n_Higgsdaughter/I')
    t_out.Branch('m_n_neutrino',m_n_neutrino,'m_n_neutrino/I')
    t_out.Branch('m_m_dimu',m_m_dimu,'m_m_dimu/F')
    t_out.Branch('m_m_recoil',m_m_recoil,'m_m_recoil/F')
    t_out.Branch('m_phi_dilepton_1',m_phi_dilepton_1,'m_phi_dilepton_1/F')
    t_out.Branch('m_phi_dilepton_2',m_phi_dilepton_2,'m_phi_dilepton_2/F')
    t_out.Branch('m_cos_miss',m_cos_miss,'m_cos_miss/F')
    t_out.Branch('m_cos_Z',m_cos_Z,'m_cos_Z/F')
    t_out.Branch('m_theta_dilepton',m_theta_dilepton,'m_theta_dilepton/F')
    t_out.Branch('m_cos_theta_leptonm',m_cos_theta_leptonm,'m_cos_theta_leptonm/F')
    t_out.Branch('m_cos_theta_leptonp',m_cos_theta_leptonp,'m_cos_theta_leptonp/F')
    t_out.Branch('m_angle_dilepton',m_angle_dilepton,'m_angle_dilepton/F')
    t_out.Branch('m_delta_pt',m_delta_pt,'m_delta_pt/F')
    t_out.Branch('m_energy_neutrino',m_energy_neutrino,'m_energy_neutrino/F')
    t_out.Branch('m_p_visible',m_p_visible,'m_p_visible[4]/F')
    t_out.Branch('m_p_visible3',m_p_visible3,'m_p_visible3/F')
    t_out.Branch('m_energy_visible',m_energy_visible,'m_energy_visible/F')
    t_out.Branch('m_miss_m',m_miss_m,'m_miss_m/F')
    t_out.Branch('m_miss_e',m_miss_e,'m_miss_e/F')


    t_out.Branch('m_e_other',m_e_other,'m_e_other/F')
    t_out.Branch('m_m_visible',m_m_visible,'m_m_visible/F')
    t_out.Branch('m_e_dimu',m_e_dimu,'m_e_dimu/F')
    t_out.Branch('m_e_recoil',m_e_recoil,'m_e_recoil/F')
    t_out.Branch('m_mine_lepton',m_mine_lepton,'m_mine_lepton/F')
    t_out.Branch('m_maxe_lepton',m_maxe_lepton,'m_maxe_lepton/F')
    t_out.Branch('m_minp_lepton',m_minp_lepton,'m_minp_lepton[4]/F')
    t_out.Branch('m_maxp_lepton',m_maxp_lepton,'m_maxp_lepton[4]/F')  

    t_out.Branch('m_miss_p',m_miss_p,'m_miss_p/F')
    t_out.Branch('m_p_dimu',m_p_dimu,'m_p_dimu/F')
    t_out.Branch('m_p_recoil',m_p_recoil,'m_p_recoil/F')  
    
#Mc information
    t_out.Branch("mc_pdgid", m_mc_pdgid)
    t_out.Branch("mc_init_pdgid", m_mc_init_pdgid)
    
    t_out.Branch("mc_lepton_minus_id", m_mc_lepton_minus_id, "mc_lepton_minus_id/I")
    t_out.Branch("mc_lepton_plus_id", m_mc_lepton_plus_id, "mc_lepton_plus_id/I")
    
    t_out.Branch("mc_init_n_lepton_plus", m_mc_init_n_lepton_plus,  "mc_init_n_lepton_plus/I")
    t_out.Branch("mc_init_n_lepton_minus", m_mc_init_n_lepton_minus,  "mc_init_n_lepton_minus/I")
    
    t_out.Branch("mc_init_leptonp_e",  m_mc_init_leptonp_e,   "mc_init_leptonp_e/D")
    t_out.Branch("mc_init_leptonp_p",  m_mc_init_leptonp_p,   "mc_init_leptonp_p/D")
    t_out.Branch("mc_init_leptonp_pt", m_mc_init_leptonp_pt,  "mc_init_leptonp_pt/D")
    t_out.Branch("mc_init_leptonp_pz", m_mc_init_leptonp_pz,  "mc_init_leptonp_pz/D")

    t_out.Branch("mc_init_leptonp_phi", m_mc_init_leptonp_phi,  "mc_init_leptonp_phi/D")
    t_out.Branch("mc_init_leptonp_theta", m_mc_init_leptonp_theta,  "mc_init_leptonp_theta/D")
    
    t_out.Branch("mc_init_leptonm_e",  m_mc_init_leptonm_e,   "mc_init_leptonm_e/D")
    t_out.Branch("mc_init_leptonm_p",  m_mc_init_leptonm_p,   "mc_init_leptonm_p/D")
    t_out.Branch("mc_init_leptonm_pt", m_mc_init_leptonm_pt,  "mc_init_leptonm_pt/D")
    t_out.Branch("mc_init_leptonm_pz", m_mc_init_leptonm_pz,  "mc_init_leptonm_pz/D")

    t_out.Branch("mc_init_leptonm_phi", m_mc_init_leptonm_phi,  "mc_init_leptonm_phi/D")
    t_out.Branch("mc_init_leptonm_theta", m_mc_init_leptonm_theta,  "mc_init_leptonm_theta/D")
    
    t_out.Branch("mc_init_dilepton_m",  m_mc_init_dilepton_m,   "mc_init_dilepton_m/D")
    t_out.Branch("mc_init_dilepton_e",  m_mc_init_dilepton_e,   "mc_init_dilepton_e/D")
    t_out.Branch("mc_init_dilepton_p",  m_mc_init_dilepton_p,   "mc_init_dilepton_p/D")
    t_out.Branch("mc_init_dilepton_pt", m_mc_init_dilepton_pt,  "mc_init_dilepton_pt/D")
    t_out.Branch("mc_init_dilepton_pz", m_mc_init_dilepton_pz,  "mc_init_dilepton_pz/D")
    t_out.Branch("mc_init_dilepton_rec_m", m_mc_init_dilepton_rec_m,  "mc_init_dilepton_rec_m/D")
    t_out.Branch("mc_init_dilepton_dphi", m_mc_init_dilepton_dphi,  "mc_init_dilepton_dphi/D")
    t_out.Branch("mc_init_dilepton_dang", m_mc_init_dilepton_dang,  "mc_init_dilepton_dang/D")
    
    t_out.Branch("mc_init_n_photon", m_mc_init_n_photon,  "mc_init_n_photon/I")
    t_out.Branch("mc_init_photon_e",  m_mc_init_photon_e)
    t_out.Branch("mc_init_photon_p",  m_mc_init_photon_p)
    t_out.Branch("mc_init_photon_pt",  m_mc_init_photon_pt)
    t_out.Branch("mc_init_photon_pz",  m_mc_init_photon_pz)
    t_out.Branch("mc_init_photon_phi",  m_mc_init_photon_phi)
    t_out.Branch("mc_init_photon_theta",  m_mc_init_photon_theta)

    t_out.Branch("mc_higgs_m", m_mc_higgs_m, "mc_higgs_m/D")
    t_out.Branch("mc_higgs_e", m_mc_higgs_e, "mc_higgs_e/D")
    t_out.Branch("mc_higgs_rec_m", m_mc_higgs_rec_m, "mc_higgs_rec_m/D")
    t_out.Branch("mc_higgs_decay_type", m_mc_higgs_decay_type, "mc_higgs_decay_type/I")
    t_out.Branch("mc_higgs_daughter_pdgid", m_mc_higgs_daughter_pdgid)
    
    t_out.Branch("mc_n_Zboson", m_mc_n_Zboson, "mc_n_Zboson/I")
    
    t_out.Branch("mc_z1_daughter_pid", m_mc_z1_daughter_pid)
    t_out.Branch("mc_z2_daughter_pid", m_mc_z2_daughter_pid)

    t_out.Branch("mc_w1_daughter_pid", m_mc_w1_daughter_pid)
    t_out.Branch("mc_w2_daughter_pid", m_mc_w2_daughter_pid)
    
    t_out.Branch("mc_zw1_m", m_mc_zw1_m, "mc_zw1_m/D")
    t_out.Branch("mc_zw1_p", m_mc_zw1_p, "mc_zw1_p/D")
    t_out.Branch("mc_zw1_pt", m_mc_zw1_pt, "mc_zw1_pt/D")
    t_out.Branch("mc_zw1_e", m_mc_zw1_e, "mc_zw1_e/D")
    t_out.Branch("mc_zw1_rec_m", m_mc_zw1_rec_m, "mc_zw1_rec_m/D")
    
    t_out.Branch("mc_zw2_m", m_mc_zw2_m, "mc_zw2_m/D")
    t_out.Branch("mc_zw2_p", m_mc_zw2_p, "mc_zw2_p/D")
    t_out.Branch("mc_zw2_pt", m_mc_zw2_pt, "mc_zw2_pt/D")
    t_out.Branch("mc_zw2_e", m_mc_zw2_e, "mc_zw2_e/D")
    t_out.Branch("mc_zw2_rec_m", m_mc_zw2_rec_m, "mc_zw2_rec_m/D")
    
    t_out.Branch("mc_zw1zw2_m", m_mc_zw1zw2_m, "mc_zw1zw2_m/D")
    t_out.Branch("mc_zw1zw2_e", m_mc_zw1zw2_e, "mc_zw1zw2_e/D")
    t_out.Branch("mc_zw1zw2_rec_m", m_mc_zw1zw2_rec_m, "mc_zw1zw2_rec_m/D")
    t_out.Branch("mc_zz_flag", m_mc_zz_flag, "mc_zz_flag/I")
    t_out.Branch("mc_ww_flag", m_mc_ww_flag, "mc_ww_flag/I")
    t_out.Branch("mc_h2gaugeboson_flag", m_mc_h2gaugeboson_flag, "mc_h2gaugeboson_flag/I")
    #tau information 
    t_out.Branch("nTau", _nTau, "nTau/I");
    t_out.Branch("nTauP", _nTauP, "nTauP/I");
    t_out.Branch("nTauM", _nTauM,"nTauM/I");
    t_out.Branch("fakeTau", _fakeTau, "fakeTau/I");
    t_out.Branch("totalJet", _totalJet, "totalJet/I");

    t_out.Branch("visEp",_visEp,"visEp/F");
    t_out.Branch("visEm",_visEm, "visEm/F");

    t_out.Branch("invMp",_invMp,"invMp/F");
    t_out.Branch("invMm",_invMm,"invMm/F");

    t_out.Branch("evtN",_evtN,"evtN/I");
    t_out.Branch("TauTauImpact",_TauTauImpact, "TauTauImpact/F");
    t_out.Branch("TauTauD0",_TauTauD0, "TauTauD0/F");
    t_out.Branch("TauTauZ0", _TauTauZ0, "TauTauZ0/F");
    t_out.Branch("tauP_impact", _tauP_impact, "tauP_impact/F");
    t_out.Branch("tauM_impact", _tauM_impact, "tauM_impact/F");
    t_out.Branch("RecoilM", _RecoilM, "RecoilM/F");
    t_out.Branch("qqRecoilM", _qqRecoilM,"qqRecoilM/F");
    t_out.Branch("TauTauM",  _TauTauM,"TauTauM/F");
    t_out.Branch("qqM",_qqM,"qqM/F");
    t_out.Branch("TotalEvtEn",_TotalEvtEn,"TotalEvtEn/F");

    for i in xrange(entries):
        if (weight<1):
            rnd=random.random()
            if (rnd<weight):
                t_in.GetEntry(i)
                t_out.Fill()
        else :
            rnd1=random.random()

            valuem=int(weight)
            dweight=abs(valuem-weight)

            if (rnd1<dweight):
                for j in xrange(int(weight)+1):
                    t_in.GetEntry(i)
                    t_out.Fill()
            else:
                for j in xrange(int(weight)):
                    t_in.GetEntry(i)
                    t_out.Fill()
    for i in xrange(0,63):
        h[i].Write()
    h_evtflw.Write()
    t_out.Write()
    m_mc_init_photon_e.clear()
    m_mc_init_photon_p.clear()
    m_mc_init_photon_pt.clear()
    m_mc_init_photon_pz.clear()
    m_mc_init_photon_phi.clear()
    m_mc_init_photon_theta.clear()

    m_mc_z1_daughter_pid.clear()
    m_mc_z2_daughter_pid.clear()
    m_mc_pdgid.clear()
    m_mc_init_pdgid.clear()
    m_mc_w1_daughter_pid.clear()
    m_mc_w2_daughter_pid.clear()
    m_mc_higgs_daughter_pdgid.clear()
if __name__ == '__main__':
    main()
