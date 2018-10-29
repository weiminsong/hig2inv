#!/usr/bin/env bash        

# Main driver to submit jobs 
# Author SHI Xin <shixin@ihep.ac.cn> 
# Created [2016-08-16 Tue 08:29] 

usage() {
    printf "NAME\n\tsubmit.sh - Main driver to submit jobs\n"
    printf "\nSYNOPSIS\n"
    printf "\n\t%-5s\n" "./submit.sh [OPTION]" 
    printf "\nOPTIONS\n" 
    printf "\n\t%-5s  %-40s\n"  "0.1.1"    "Run on signal and background samples" 
    printf "\n\t%-5s  %-40s\n"  "0.1.2"    "Synthetize seperated ROOT files" 
    printf "\n\t%-5s  %-40s\n"  "0.1.3"    "Draw distributions of cut variables and calculate ratios of bachground over signal" 
    printf "\n\t%-5s  %-40s\n"  "0.1.4"    "Calculate cut flows of siganl and background samples" 
    printf "\n\t%-5s  %-40s\n"  "0.1.5"    "Apply BDT cut"
    printf "\n\t%-5s  %-40s\n"  "0.1.6"    "Synthetize signal and background ROOT files"
    printf "\n\t%-5s  %-40s\n"  "0.1.7"    "Fit higggs mass spectra(recoilling mass of Z boson)"
    printf "\n\t%-5s  %-40s\n"  "0.1.8"    "Calculate upper limmits of branch ratio"
        
    #0.2 #mumuH_invisible
    printf "\n\t%-5s  %-40s\n"  "0.2"      "Runing signal samples..."
    printf "\n\t%-5s  %-40s\n"  "0.2.1"    "Split signal sample with each group 0.5G..."  
    printf "\n\t%-5s  %-40s\n"  "0.2.2"    "Generate XML input files for Marlin job..."
    printf "\n\t%-5s  %-40s\n"  "0.2.3"    "Run with a few events" 
    printf "\n\t%-5s  %-40s\n"  "0.2.4"    "Generate Condor job scripts..." 
    printf "\n\t%-5s  %-40s\n"  "0.2.5"    "Submit Condor jobs for pre-selection on signal..."
    printf "\n\t%-5s  %-40s\n"  "0.2.6"    "Select events on signal (with a small sample)..."
    printf "\n\t%-5s  %-40s\n"  "0.2.7"    "Generate Condor job scripts for event selection..."
    printf "\n\t%-5s  %-40s\n"  "0.2.8"    "Submit Condor jobs for event selection on signal..."
    printf "\n\t%-5s  %-40s\n"  "0.2.9"    "Merge event root files..."         
    #0.3 #background
    printf "\n\t%-5s  %-40s\n"  "0.3"      "Running on background sample...."
    printf "\n\t%-5s  %-40s\n"  "0.3.1"    "Split background sample with each group 20G..."  
    printf "\n\t%-5s  %-40s\n"  "0.3.2"    "Generate XML input files for Marlin job..."
    printf "\n\t%-5s  %-40s\n"  "0.3.3"    "Check statistics : print the number of files..." 
    printf "\n\t%-5s  %-40s\n"  "0.3.4"    "GRun with a few events ..." 
    printf "\n\t%-5s  %-40s\n"  "0.3.5"    "Generate Condor job scripts..."
    printf "\n\t%-5s  %-40s\n"  "0.3.6"    "Submit Condor jobs for pre-selection on background sample..."
    printf "\n\t%-5s  %-40s\n"  "0.3.7"    "Select events on background (with a small sample)..."
    printf "\n\t%-5s  %-40s\n"  "0.3.8"    "Generate Condor job scripts for event selection..."
    printf "\n\t%-5s  %-40s\n"  "0.3.9"    "Submit Condor jobs for pre-selection on background sample..." 
    printf "\n\t%-5s  %-40s\n"  "0.3.10"   "Merge event root files..." 
    printf "\n\t%-5s  %-40s\n"  "0.3.11"   "Plot signal and background cut distribution"
    printf "\n\t%-5s  %-40s\n"  "0.3.12"   "Plot before cut and after cut distribution" 
    printf "\n\t%-5s  %-40s\n"  "0.3.13"   "Expand the background two times" 
    printf "\n\t%-5s  %-40s\n"  "0.3.14"   "Applying BDT cut..."
    printf "\n\t%-5s  %-40s\n"  "0.3.15"   "Synthetizing signal and background ROOT files..."
	printf "\n\t%-5s  %-40s\n"  "0.3.16"   "Fitting higgs mass spectra(recoilling mass of Z boson)..."
    printf "\n\t%-5s  %-40s\n"  "0.3.17"   "Calculating upper limmit of branch ratio..."

    printf "\nDATE\n"
    printf "\n\t%-5s\n" "AUGUST 2016"     
}


if [[ $# -eq 0 ]]; then
    usage
fi

signal_slcio_dir=/cefs/data/DstData/CEPC240/CEPC_v4/higgs/smart_final_states/E240.Pffh_invi.e0.p0.whizard195/

sel_all=0
sel_signal=1
sel_bg=2


option=$1

case $option in 
    0.1.1) echo "Running on signal and background samples..."
        if [ ! -d "steer" ]; then
            mkdir steer
        fi
        if [ ! -d "splitted" ]; then
            mkdir splitted
        fi
        rm job/job.out -rf
        mkdir  job/job.out
        rm job/job.err -rf
        mkdir job/job.err
        cd job
        bash run_sample
    ;;

    0.1.2) echo "Synthetizing seperated ROOT files..."
        if [ ! -d "presel" ]; then
            mkdir presel
        fi
        cd job
        ./hadd.sh
    ;;

    0.1.3) echo "Drawing distributions of cut variables and calculate ratios of bachground over signal..."
        if [ ! -d "figs" ]; then
            mkdir figs
        fi
        if [ ! -d "logfiles" ]; then
            mkdir logfiles
        fi
        cd job
        hep_sub -g physics cut_variable_job -e job.err -o job.out
    ;;

    0.1.4) echo "Calculating cut flows of siganl and background samples..."
        if [ ! -d "sel" ]; then
            mkdir sel
        fi
        if [ ! -d "logfiles" ]; then
            mkdir logfiles
        fi
        cd job
        hep_sub -g physics cut_flow_job -e job.err -o job.out
    ;;

    0.1.5) echo "Applying BDT cut..."
        if [ ! -d "BDT_output" ]; then
            mkdir BDT_output
        fi
        cd BDT
        if [ ! -f "../BDT_output/bkg_e2e2h.root" ]; then
            echo "Samples are about to be trained, after that please check the distribution to get BDT cut and run ./submit 0.1.5 again to apply that!"
            root -l Hinv.C
        else
            echo "BDT cut is about to be applied!"
            root -l -q HinvApplication.C
        fi
    ;;

    0.1.6) echo "Synthetizing signal and background ROOT files..."
        cd python
        rm ../BDT_output/Hinv_sig_e2e2h_selected_BDT.root -rf
        python chs_events.py ../BDT_output/Hinv_sig_e2e2h_2fermions_BDT.root ../BDT_output/Hinv_sig_e2e2h_selected_BDT.root signal_e2e2h
        cd ../BDT_output
        rm ../sel/sig_bkg_e2e2h.root -rf
        hadd ../sel/sig_bkg_e2e2h.root Hinv_bkg_e2e2h_2fermions_BDT.root Hinv_bkg_e2e2h_4fermions_BDT.root Hinv_sig_e2e2h_selected_BDT.root
    ;;

    0.1.7) echo "Fitting higgs mass spectra(recoilling mass of Z boson)..."
        cd src
        root fithiggs.cxx
    ;;

    0.1.8) echo "Calculating upper limmit of branch ratio..."
        cd python
        python cal_upperlimit.py
    ;;

    #example e2E2h_invisible 

   
    0.2)   echo "Runing signal samples..."
   
        ;;
 
    0.2.1) echo "Split signal sample with each group 0.5G..."
        
            mkdir -p ./run/e2E2h_invi/samples
            ./python/get_samples.py ${signal_slcio_dir} ./run/e2E2h_invi/samples/E240_Pffh_invi.txt 0.5G
        ;;       
           
    0.2.2) echo "Generate XML input files for Marlin job..."
                
            mkdir -p   ./run/e2E2h_invi/steers
            mkdir -p   ./run/e2E2h_invi/steers/test
            mkdir -p   ./run/e2E2h_invi/ana/test       
                              
            ./python/get_steerfiles.py ./table/template_jobfile.xml ./run/e2E2h_invi/samples ./run/e2E2h_invi/steers ./run/e2E2h_invi/ana/ana_File.root    
    
        ;;
           
    0.2.3) echo "Run with a few events"
                   
            source setup.sh
#           ./build.sh
            Marlin run/e2E2h_invi/steers/test/sample-1.xml
            
        ;;

    0.2.4) echo "Generate Condor job scripts..."

            mkdir -p   ./run/e2E2h_invi/condor/script/marlin
           ./python/gen_condorscripts.py  1  ./run/e2E2h_invi/steers ./run/e2E2h_invi/condor  ${sel_signal}
           
        ;;

    0.2.5) echo "Submit Condor jobs for pre-selection on signal..."
                    
            cd ./run/e2E2h_invi/condor
            mkdir -p log
            ./condor_submit.sh

        ;;

    0.2.6) echo "Select events on signal (with a small sample)..."
                
#            mkdir -p   ./run/e2E2h_invi/events/ana
            mkdir -p   ./run/e2E2h_invi/events/ana/
            ./python/sel_events.py  ./run/e2E2h_invi/ana/ana_File-2.root  ana_File-2_test.root 
            
        ;;

    0.2.7) echo "Generate Condor job scripts for event selection..."

            mkdir -p   ./run/e2E2h_invi/events/ana
            mkdir -p   ./run/e2E2h_invi/condor/script/eventsel
            ./python/gen_condorscripts.py  2  ./run/e2E2h_invi/ana ./run/e2E2h_invi/condor  

        ;;
    
    0.2.8) echo "Submit Condor jobs for event selection on signal..."

            cd ./run/e2E2h_invi/condor
            mkdir -p log/events
            ./condor_submit_eventsel.sh

  
        ;;

    0.2.9) echo  "Merge event root files..."
           
            mkdir -p   ./run/e2E2h_invi/hist

            ./python/mrg_rootfiles.py  ./run/e2E2h_invi/events/ana  ./run/e2E2h_invi/hist 

        ;;
    #background information 

    0.3) echo "Running on background sample...."

        ;;

    0.3.1) echo "Split background sample with each group 20G..."
          
            mkdir -p   ./run/bg/samples
            ./python/get_bg_samples.py ./table/bg_sample_list.txt ./run/bg/samples 20G           

        ;;           
    0.3.2) echo "Generate XML input files for Marlin job..."  

            mkdir -p   ./run/bg/steers 
            mkdir -p   ./run/bg/ana

            ./python/gen_bg_steerfiles.py ./table/bg_sample_list.txt ./table/template_jobfile.xml  ./run/bg/samples  ./run/bg/steers  ./run/bg/ana
        
        ;;
               
    0.3.3) echo "Check statistics : print the number of files..."
        
            ./python/check_stat.py  ./table/bg_sample_list.txt ./run/bg/samples 
        
       ;;

    0.3.4) echo "Run with a few events ..."
#	   source setup.sh
#	   ./build.sh
            cd ./run/bg/steers/

            array=("e3e3" "qq" "ww_l0ll" "zz_h" "zz_sl" "zz_l" "ww_h" "ww_sl" "zzorww_l" "sze_l" "sze_sl" "sznu_l" "sznu_sl" "sw_l" "sw_sl" "szeorsw_l" "e1e1" "e2e2" "n2n2" "zzorww_h") 

            for dir in "${array[@]}"            
            do
                cd ${dir}/test
                Marlin sample-1.xml
                cd ../../
            done

        ;;

    0.3.5) echo "Generate Condor job scripts..."

            mkdir -p   ./run/bg/condor
            cd ./run/bg/ana/
            for dir in *
            do
                mkdir -p ../condor/$dir
            done

            cd ../condor/
            for dir in *
            do
                cd $dir
                rm -rf log/marlin
                rm -rf script/marlin
                mkdir -p log/marlin
                mkdir -p script/marlin
                cd ../
            done

            cd ../../../
            ./python/gen_bg_condorscripts.py  1  ./run/bg/steers ./run/bg/condor  

        ;;
    
    0.3.6) echo "Submit Condor jobs for pre-selection on background sample..."
           echo " ---- "
           echo "Please enter the number of jobs for each backgrond (default: 1000)"  

            njob=1000    
            cd ./run/bg/condor
            for dir in *
            do
                cd $dir
                echo `pwd`
                ./condor_submit.sh $njob
                cd ../
            done 
           ;;
            
    0.3.7) echo "Select events on background (with a small sample)..."
            
            mkdir -p   ./run/bg/events/ana/
            cd ./run/bg/ana
            for dir in *
            do
                mkdir -p ../events/ana/$dir
            done
            cd ../../../
            #Maybe can't work 
            ./python/sel_events.py  run/bg/steers/e2e2/test/ana_bg_test_1.root  ./run/bg/steers/e2e2/test/ana_bg_test_1_event.root

           ;;

    0.3.8) echo "Generate Condor job scripts for event selection..."
   
            mkdir -p   ./run/bg/events/ana
        
            cd ./run/bg/condor

            for dir in *
            do
                mkdir -p   ../scale/$dir
                cd $dir
                rm -rf log/events
                rm -rf script/eventsel
                mkdir -p log/events
                mkdir -p script/eventsel
                cd ../
            done
       
            cd ../../../
            ./python/gen_bg_condorscripts.py  2  ./run/bg/ana ./run/bg/condor  

        ;;

    0.3.9) echo "Submit Condor jobs for pre-selection on background sample..."

            cd ./run/bg/condor
            for dir in *
            do
 #               if [$dir != test]; then                 
                cd $dir
                echo `pwd`
                ./condor_submit_eventsel.sh 
                cd ../
#                fi
            done

        ;;

    0.3.10) echo  "Merge event root files..."
            mkdir -p ./run/bg/hist
            mkdir -p ./run/bg/plot
            cd ./run/bg/scale
            for dir in *
            do
            mkdir -p ../hist/$dir
            mkdir -p ../plot/$dir
               cd ../../../
                #Merge data after scale 
               ./python/mrg_rootfiles.py  ./run/bg/scale/$dir  ./run/bg/hist/$dir
               #Merge data before scale
               ./python/mrg_rootfiles.py  ./run/bg/events/ana/$dir ./run/bg/plot/$dir
               cd ./run/bg/scale	       
           done

        ;;
    0.3.11) echo "Plot signal and background cut distribution"
            mkdir -p ./run/total
            rm ./run/total/bkg_add_sig.root -rf
            rm ./run/bg/hist/all_bkg_merge.root -rf
            rm ./run/bg/plot/all_bkg_merge.root -rf
            #merge all backgrounds;merge backgrounds and signal
            ./python/hadd.sh

        ;;
    0.3.12) echo "Plot before cut and after cut distribution"
            mkdir -p fig/after
            mkdir -p fig/before           
            ./python/plt_before_summary.py bkg+sig background signal
            ./python/plt_after_summary.py bkg+sig background signal
  
       ;;

    0.3.13) echo "Expand the background three times" 

           ./python/scale_events.py ./run/bg/hist/all_bkg_merge.root ./run/bg/hist/all_bkg_merge_scale.root all_bkg

       ;;

    0.3.14) echo "Applying BDT cut..."
            if [ ! -d "BDT_output" ]; then
                mkdir BDT_output
            fi
            cd BDT
            if [ ! -f "../BDT_output/bkg_e2e2h.root" ]; then
                echo "Samples are about to be trained, after that please check the distribution to get BDT cut and run ./submit 0.3.12 again to apply that!"
                root -l Hinv.C
            else
                echo "BDT cut is about to be applied!"
                root -l -q HinvApplication.C
            fi
    ;;

    0.3.15) echo "Synthetizing signal and background ROOT files..."
    
            rm ./BDT_output/Hinv_bkg_e2e2h_selected_BDT.root -rf
            # Expand background 62 times,make background and signal have the same scale.
            python ./python/scale_bkg_events.py ./BDT_output/Hinv_bkg_e2e2h_BDT.root ./BDT_output/Hinv_bkg_e2e2h_selected_BDT.root all_bkg

            rm  ./run/total/bkg_add_sig_BDT.root

            hadd ./run/total/bkg_add_sig_BDT.root ./BDT_output/Hinv_bkg_e2e2h_selected_BDT.root ./BDT_output/Hinv_sig_e2e2h_BDT.root
    
    ;;

    0.3.16) echo "Fitting higgs mass spectra(recoilling mass of Z boson)..."

            root ./src/fitBDT.cxx
    ;;

    0.3.17) echo "Calculating upper limit of branch ratio..."
            
            python ./python/cal_upperlimit_BDT.py
    ;;

esac    

