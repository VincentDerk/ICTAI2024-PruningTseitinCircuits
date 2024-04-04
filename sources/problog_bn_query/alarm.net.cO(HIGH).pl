%% ProbLog program: PGM 1
%% Created on 2019-05-23 15:41:52.187413
0.05::fIO2("LOW"); 0.95::fIO2("NORMAL").
0.2::hYPOVOLEMIA.
0.1::eRRCAUTER.
0.92::iNTUBATION("NORMAL"); 0.03::iNTUBATION("ESOPHAGEAL"); 0.05::iNTUBATION("ONESIDED").
0.04::kINKEDTUBE.
0.01::pULMEMBOLUS.
0.05::lVFAILURE.
0.01::aNAPHYLAXIS.
0.05::eRRLOWOUTPUT.
0.05::mINVOLSET("LOW"); 0.9::mINVOLSET("NORMAL"); 0.05::mINVOLSET("HIGH").
0.1::iNSUFFANESTH.
0.1::dISCONNECT.
0.98::tPR("LOW"); 0.01::tPR("NORMAL"); 0.01::tPR("HIGH") :- aNAPHYLAXIS.
0.3::tPR("LOW"); 0.4::tPR("NORMAL"); 0.3::tPR("HIGH") :- \+aNAPHYLAXIS.
0.9::hISTORY :- lVFAILURE.
0.01::hISTORY :- \+lVFAILURE.
0.95::lVEDVOLUME("LOW"); 0.04::lVEDVOLUME("NORMAL"); 0.01::lVEDVOLUME("HIGH") :- hYPOVOLEMIA, lVFAILURE.
0.01::lVEDVOLUME("LOW"); 0.09::lVEDVOLUME("NORMAL"); 0.9::lVEDVOLUME("HIGH") :- hYPOVOLEMIA, \+lVFAILURE.
0.98::lVEDVOLUME("LOW"); 0.01::lVEDVOLUME("NORMAL"); 0.01::lVEDVOLUME("HIGH") :- \+hYPOVOLEMIA, lVFAILURE.
0.05::lVEDVOLUME("LOW"); 0.9::lVEDVOLUME("NORMAL"); 0.05::lVEDVOLUME("HIGH") :- \+hYPOVOLEMIA, \+lVFAILURE.
0.05::vENTMACH("ZERO"); 0.93::vENTMACH("LOW"); 0.01::vENTMACH("NORMAL"); 0.01::vENTMACH("HIGH") :- mINVOLSET("LOW").
0.05::vENTMACH("ZERO"); 0.01::vENTMACH("LOW"); 0.93::vENTMACH("NORMAL"); 0.01::vENTMACH("HIGH") :- mINVOLSET("NORMAL").
0.05::vENTMACH("ZERO"); 0.01::vENTMACH("LOW"); 0.01::vENTMACH("NORMAL"); 0.93::vENTMACH("HIGH") :- mINVOLSET("HIGH").
0.1::sHUNT("NORMAL"); 0.9::sHUNT("HIGH") :- iNTUBATION("NORMAL"), pULMEMBOLUS.
0.95::sHUNT("NORMAL"); 0.05::sHUNT("HIGH") :- iNTUBATION("NORMAL"), \+pULMEMBOLUS.
0.1::sHUNT("NORMAL"); 0.9::sHUNT("HIGH") :- iNTUBATION("ESOPHAGEAL"), pULMEMBOLUS.
0.95::sHUNT("NORMAL"); 0.05::sHUNT("HIGH") :- iNTUBATION("ESOPHAGEAL"), \+pULMEMBOLUS.
0.01::sHUNT("NORMAL"); 0.99::sHUNT("HIGH") :- iNTUBATION("ONESIDED"), pULMEMBOLUS.
0.05::sHUNT("NORMAL"); 0.95::sHUNT("HIGH") :- iNTUBATION("ONESIDED"), \+pULMEMBOLUS.
0.98::sTROKEVOLUME("LOW"); 0.01::sTROKEVOLUME("NORMAL"); 0.01::sTROKEVOLUME("HIGH") :- hYPOVOLEMIA, lVFAILURE.
0.5::sTROKEVOLUME("LOW"); 0.49::sTROKEVOLUME("NORMAL"); 0.01::sTROKEVOLUME("HIGH") :- hYPOVOLEMIA, \+lVFAILURE.
0.95::sTROKEVOLUME("LOW"); 0.04::sTROKEVOLUME("NORMAL"); 0.01::sTROKEVOLUME("HIGH") :- \+hYPOVOLEMIA, lVFAILURE.
0.05::sTROKEVOLUME("LOW"); 0.9::sTROKEVOLUME("NORMAL"); 0.05::sTROKEVOLUME("HIGH") :- \+hYPOVOLEMIA, \+lVFAILURE.
0.01::pAP("LOW"); 0.19::pAP("NORMAL"); 0.8::pAP("HIGH") :- pULMEMBOLUS.
0.05::pAP("LOW"); 0.9::pAP("NORMAL"); 0.05::pAP("HIGH") :- \+pULMEMBOLUS.
0.97::vENTTUBE("ZERO"); 0.01::vENTTUBE("LOW"); 0.01::vENTTUBE("NORMAL"); 0.01::vENTTUBE("HIGH") :- dISCONNECT, vENTMACH("ZERO").
0.97::vENTTUBE("ZERO"); 0.01::vENTTUBE("LOW"); 0.01::vENTTUBE("NORMAL"); 0.01::vENTTUBE("HIGH") :- dISCONNECT, vENTMACH("LOW").
0.97::vENTTUBE("ZERO"); 0.01::vENTTUBE("LOW"); 0.01::vENTTUBE("NORMAL"); 0.01::vENTTUBE("HIGH") :- dISCONNECT, vENTMACH("NORMAL").
0.01::vENTTUBE("ZERO"); 0.01::vENTTUBE("LOW"); 0.97::vENTTUBE("NORMAL"); 0.01::vENTTUBE("HIGH") :- dISCONNECT, vENTMACH("HIGH").
0.97::vENTTUBE("ZERO"); 0.01::vENTTUBE("LOW"); 0.01::vENTTUBE("NORMAL"); 0.01::vENTTUBE("HIGH") :- \+dISCONNECT, vENTMACH("ZERO").
0.97::vENTTUBE("ZERO"); 0.01::vENTTUBE("LOW"); 0.01::vENTTUBE("NORMAL"); 0.01::vENTTUBE("HIGH") :- \+dISCONNECT, vENTMACH("LOW").
0.01::vENTTUBE("ZERO"); 0.97::vENTTUBE("LOW"); 0.01::vENTTUBE("NORMAL"); 0.01::vENTTUBE("HIGH") :- \+dISCONNECT, vENTMACH("NORMAL").
0.01::vENTTUBE("ZERO"); 0.01::vENTTUBE("LOW"); 0.01::vENTTUBE("NORMAL"); 0.97::vENTTUBE("HIGH") :- \+dISCONNECT, vENTMACH("HIGH").
0.95::pCWP("LOW"); 0.04::pCWP("NORMAL"); 0.01::pCWP("HIGH") :- lVEDVOLUME("LOW").
0.04::pCWP("LOW"); 0.95::pCWP("NORMAL"); 0.01::pCWP("HIGH") :- lVEDVOLUME("NORMAL").
0.01::pCWP("LOW"); 0.04::pCWP("NORMAL"); 0.95::pCWP("HIGH") :- lVEDVOLUME("HIGH").
0.95::cVP("LOW"); 0.04::cVP("NORMAL"); 0.01::cVP("HIGH") :- lVEDVOLUME("LOW").
0.04::cVP("LOW"); 0.95::cVP("NORMAL"); 0.01::cVP("HIGH") :- lVEDVOLUME("NORMAL").
0.01::cVP("LOW"); 0.29::cVP("NORMAL"); 0.7::cVP("HIGH") :- lVEDVOLUME("HIGH").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("NORMAL"), kINKEDTUBE, vENTTUBE("ZERO").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("NORMAL"), kINKEDTUBE, vENTTUBE("LOW").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("NORMAL"), kINKEDTUBE, vENTTUBE("NORMAL").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("NORMAL"), kINKEDTUBE, vENTTUBE("HIGH").
0.3::vENTLUNG("ZERO"); 0.68::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("NORMAL"), \+kINKEDTUBE, vENTTUBE("ZERO").
0.95::vENTLUNG("ZERO"); 0.03::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("NORMAL"), \+kINKEDTUBE, vENTTUBE("LOW").
0.01::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.97::vENTLUNG("HIGH") :- iNTUBATION("NORMAL"), \+kINKEDTUBE, vENTTUBE("NORMAL").
0.01::vENTLUNG("ZERO"); 0.97::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("NORMAL"), \+kINKEDTUBE, vENTTUBE("HIGH").
0.95::vENTLUNG("ZERO"); 0.03::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ESOPHAGEAL"), kINKEDTUBE, vENTTUBE("ZERO").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ESOPHAGEAL"), kINKEDTUBE, vENTTUBE("LOW").
0.01::vENTLUNG("ZERO"); 0.97::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ESOPHAGEAL"), kINKEDTUBE, vENTTUBE("NORMAL").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ESOPHAGEAL"), kINKEDTUBE, vENTTUBE("HIGH").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ESOPHAGEAL"), \+kINKEDTUBE, vENTTUBE("ZERO").
0.5::vENTLUNG("ZERO"); 0.48::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ESOPHAGEAL"), \+kINKEDTUBE, vENTTUBE("LOW").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ESOPHAGEAL"), \+kINKEDTUBE, vENTTUBE("NORMAL").
0.01::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.97::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ESOPHAGEAL"), \+kINKEDTUBE, vENTTUBE("HIGH").
0.4::vENTLUNG("ZERO"); 0.58::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ONESIDED"), kINKEDTUBE, vENTTUBE("ZERO").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ONESIDED"), kINKEDTUBE, vENTTUBE("LOW").
0.01::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.97::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ONESIDED"), kINKEDTUBE, vENTTUBE("NORMAL").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ONESIDED"), kINKEDTUBE, vENTTUBE("HIGH").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ONESIDED"), \+kINKEDTUBE, vENTTUBE("ZERO").
0.3::vENTLUNG("ZERO"); 0.68::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ONESIDED"), \+kINKEDTUBE, vENTTUBE("LOW").
0.97::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.01::vENTLUNG("HIGH") :- iNTUBATION("ONESIDED"), \+kINKEDTUBE, vENTTUBE("NORMAL").
0.01::vENTLUNG("ZERO"); 0.01::vENTLUNG("LOW"); 0.01::vENTLUNG("NORMAL"); 0.97::vENTLUNG("HIGH") :- iNTUBATION("ONESIDED"), \+kINKEDTUBE, vENTTUBE("HIGH").
0.97::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("NORMAL"), kINKEDTUBE, vENTTUBE("ZERO").
0.05::pRESS("ZERO"); 0.25::pRESS("LOW"); 0.25::pRESS("NORMAL"); 0.45::pRESS("HIGH") :- iNTUBATION("NORMAL"), kINKEDTUBE, vENTTUBE("LOW").
0.97::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("NORMAL"), kINKEDTUBE, vENTTUBE("NORMAL").
0.2::pRESS("ZERO"); 0.75::pRESS("LOW"); 0.04::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("NORMAL"), kINKEDTUBE, vENTTUBE("HIGH").
0.01::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.97::pRESS("HIGH") :- iNTUBATION("NORMAL"), \+kINKEDTUBE, vENTTUBE("ZERO").
0.01::pRESS("ZERO"); 0.29::pRESS("LOW"); 0.3::pRESS("NORMAL"); 0.4::pRESS("HIGH") :- iNTUBATION("NORMAL"), \+kINKEDTUBE, vENTTUBE("LOW").
0.01::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.97::pRESS("HIGH") :- iNTUBATION("NORMAL"), \+kINKEDTUBE, vENTTUBE("NORMAL").
0.01::pRESS("ZERO"); 0.9::pRESS("LOW"); 0.08::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("NORMAL"), \+kINKEDTUBE, vENTTUBE("HIGH").
0.01::pRESS("ZERO"); 0.3::pRESS("LOW"); 0.49::pRESS("NORMAL"); 0.2::pRESS("HIGH") :- iNTUBATION("ESOPHAGEAL"), kINKEDTUBE, vENTTUBE("ZERO").
0.01::pRESS("ZERO"); 0.15::pRESS("LOW"); 0.25::pRESS("NORMAL"); 0.59::pRESS("HIGH") :- iNTUBATION("ESOPHAGEAL"), kINKEDTUBE, vENTTUBE("LOW").
0.01::pRESS("ZERO"); 0.97::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("ESOPHAGEAL"), kINKEDTUBE, vENTTUBE("NORMAL").
0.2::pRESS("ZERO"); 0.7::pRESS("LOW"); 0.09::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("ESOPHAGEAL"), kINKEDTUBE, vENTTUBE("HIGH").
0.97::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("ESOPHAGEAL"), \+kINKEDTUBE, vENTTUBE("ZERO").
0.01::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.08::pRESS("NORMAL"); 0.9::pRESS("HIGH") :- iNTUBATION("ESOPHAGEAL"), \+kINKEDTUBE, vENTTUBE("LOW").
0.97::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("ESOPHAGEAL"), \+kINKEDTUBE, vENTTUBE("NORMAL").
0.01::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.38::pRESS("NORMAL"); 0.6::pRESS("HIGH") :- iNTUBATION("ESOPHAGEAL"), \+kINKEDTUBE, vENTTUBE("HIGH").
0.01::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.08::pRESS("NORMAL"); 0.9::pRESS("HIGH") :- iNTUBATION("ONESIDED"), kINKEDTUBE, vENTTUBE("ZERO").
0.97::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("ONESIDED"), kINKEDTUBE, vENTTUBE("LOW").
0.01::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.97::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("ONESIDED"), kINKEDTUBE, vENTTUBE("NORMAL").
0.97::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("ONESIDED"), kINKEDTUBE, vENTTUBE("HIGH").
0.1::pRESS("ZERO"); 0.84::pRESS("LOW"); 0.05::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("ONESIDED"), \+kINKEDTUBE, vENTTUBE("ZERO").
0.01::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.97::pRESS("HIGH") :- iNTUBATION("ONESIDED"), \+kINKEDTUBE, vENTTUBE("LOW").
0.4::pRESS("ZERO"); 0.58::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.01::pRESS("HIGH") :- iNTUBATION("ONESIDED"), \+kINKEDTUBE, vENTTUBE("NORMAL").
0.01::pRESS("ZERO"); 0.01::pRESS("LOW"); 0.01::pRESS("NORMAL"); 0.97::pRESS("HIGH") :- iNTUBATION("ONESIDED"), \+kINKEDTUBE, vENTTUBE("HIGH").
0.97::mINVOL("ZERO"); 0.01::mINVOL("LOW"); 0.01::mINVOL("NORMAL"); 0.01::mINVOL("HIGH") :- iNTUBATION("NORMAL"), vENTLUNG("ZERO").
0.01::mINVOL("ZERO"); 0.01::mINVOL("LOW"); 0.01::mINVOL("NORMAL"); 0.97::mINVOL("HIGH") :- iNTUBATION("NORMAL"), vENTLUNG("LOW").
0.5::mINVOL("ZERO"); 0.48::mINVOL("LOW"); 0.01::mINVOL("NORMAL"); 0.01::mINVOL("HIGH") :- iNTUBATION("NORMAL"), vENTLUNG("NORMAL").
0.01::mINVOL("ZERO"); 0.97::mINVOL("LOW"); 0.01::mINVOL("NORMAL"); 0.01::mINVOL("HIGH") :- iNTUBATION("NORMAL"), vENTLUNG("HIGH").
0.01::mINVOL("ZERO"); 0.97::mINVOL("LOW"); 0.01::mINVOL("NORMAL"); 0.01::mINVOL("HIGH") :- iNTUBATION("ESOPHAGEAL"), vENTLUNG("ZERO").
0.97::mINVOL("ZERO"); 0.01::mINVOL("LOW"); 0.01::mINVOL("NORMAL"); 0.01::mINVOL("HIGH") :- iNTUBATION("ESOPHAGEAL"), vENTLUNG("LOW").
0.5::mINVOL("ZERO"); 0.48::mINVOL("LOW"); 0.01::mINVOL("NORMAL"); 0.01::mINVOL("HIGH") :- iNTUBATION("ESOPHAGEAL"), vENTLUNG("NORMAL").
0.01::mINVOL("ZERO"); 0.01::mINVOL("LOW"); 0.97::mINVOL("NORMAL"); 0.01::mINVOL("HIGH") :- iNTUBATION("ESOPHAGEAL"), vENTLUNG("HIGH").
0.01::mINVOL("ZERO"); 0.01::mINVOL("LOW"); 0.97::mINVOL("NORMAL"); 0.01::mINVOL("HIGH") :- iNTUBATION("ONESIDED"), vENTLUNG("ZERO").
0.6::mINVOL("ZERO"); 0.38::mINVOL("LOW"); 0.01::mINVOL("NORMAL"); 0.01::mINVOL("HIGH") :- iNTUBATION("ONESIDED"), vENTLUNG("LOW").
0.97::mINVOL("ZERO"); 0.01::mINVOL("LOW"); 0.01::mINVOL("NORMAL"); 0.01::mINVOL("HIGH") :- iNTUBATION("ONESIDED"), vENTLUNG("NORMAL").
0.01::mINVOL("ZERO"); 0.01::mINVOL("LOW"); 0.01::mINVOL("NORMAL"); 0.97::mINVOL("HIGH") :- iNTUBATION("ONESIDED"), vENTLUNG("HIGH").
0.97::vENTALV("ZERO"); 0.01::vENTALV("LOW"); 0.01::vENTALV("NORMAL"); 0.01::vENTALV("HIGH") :- iNTUBATION("NORMAL"), vENTLUNG("ZERO").
0.01::vENTALV("ZERO"); 0.01::vENTALV("LOW"); 0.01::vENTALV("NORMAL"); 0.97::vENTALV("HIGH") :- iNTUBATION("NORMAL"), vENTLUNG("LOW").
0.01::vENTALV("ZERO"); 0.01::vENTALV("LOW"); 0.97::vENTALV("NORMAL"); 0.01::vENTALV("HIGH") :- iNTUBATION("NORMAL"), vENTLUNG("NORMAL").
0.03::vENTALV("ZERO"); 0.95::vENTALV("LOW"); 0.01::vENTALV("NORMAL"); 0.01::vENTALV("HIGH") :- iNTUBATION("NORMAL"), vENTLUNG("HIGH").
0.01::vENTALV("ZERO"); 0.97::vENTALV("LOW"); 0.01::vENTALV("NORMAL"); 0.01::vENTALV("HIGH") :- iNTUBATION("ESOPHAGEAL"), vENTLUNG("ZERO").
0.97::vENTALV("ZERO"); 0.01::vENTALV("LOW"); 0.01::vENTALV("NORMAL"); 0.01::vENTALV("HIGH") :- iNTUBATION("ESOPHAGEAL"), vENTLUNG("LOW").
0.01::vENTALV("ZERO"); 0.01::vENTALV("LOW"); 0.01::vENTALV("NORMAL"); 0.97::vENTALV("HIGH") :- iNTUBATION("ESOPHAGEAL"), vENTLUNG("NORMAL").
0.01::vENTALV("ZERO"); 0.94::vENTALV("LOW"); 0.04::vENTALV("NORMAL"); 0.01::vENTALV("HIGH") :- iNTUBATION("ESOPHAGEAL"), vENTLUNG("HIGH").
0.01::vENTALV("ZERO"); 0.01::vENTALV("LOW"); 0.97::vENTALV("NORMAL"); 0.01::vENTALV("HIGH") :- iNTUBATION("ONESIDED"), vENTLUNG("ZERO").
0.01::vENTALV("ZERO"); 0.97::vENTALV("LOW"); 0.01::vENTALV("NORMAL"); 0.01::vENTALV("HIGH") :- iNTUBATION("ONESIDED"), vENTLUNG("LOW").
0.97::vENTALV("ZERO"); 0.01::vENTALV("LOW"); 0.01::vENTALV("NORMAL"); 0.01::vENTALV("HIGH") :- iNTUBATION("ONESIDED"), vENTLUNG("NORMAL").
0.01::vENTALV("ZERO"); 0.88::vENTALV("LOW"); 0.1::vENTALV("NORMAL"); 0.01::vENTALV("HIGH") :- iNTUBATION("ONESIDED"), vENTLUNG("HIGH").
1.0::pVSAT("LOW"); 0.0::pVSAT("NORMAL"); 0.0::pVSAT("HIGH") :- fIO2("LOW"), vENTALV("ZERO").
0.95::pVSAT("LOW"); 0.04::pVSAT("NORMAL"); 0.01::pVSAT("HIGH") :- fIO2("LOW"), vENTALV("LOW").
1.0::pVSAT("LOW"); 0.0::pVSAT("NORMAL"); 0.0::pVSAT("HIGH") :- fIO2("LOW"), vENTALV("NORMAL").
0.01::pVSAT("LOW"); 0.95::pVSAT("NORMAL"); 0.04::pVSAT("HIGH") :- fIO2("LOW"), vENTALV("HIGH").
0.99::pVSAT("LOW"); 0.01::pVSAT("NORMAL"); 0.0::pVSAT("HIGH") :- fIO2("NORMAL"), vENTALV("ZERO").
0.95::pVSAT("LOW"); 0.04::pVSAT("NORMAL"); 0.01::pVSAT("HIGH") :- fIO2("NORMAL"), vENTALV("LOW").
0.95::pVSAT("LOW"); 0.04::pVSAT("NORMAL"); 0.01::pVSAT("HIGH") :- fIO2("NORMAL"), vENTALV("NORMAL").
0.01::pVSAT("LOW"); 0.01::pVSAT("NORMAL"); 0.98::pVSAT("HIGH") :- fIO2("NORMAL"), vENTALV("HIGH").
0.01::aRTCO2("LOW"); 0.01::aRTCO2("NORMAL"); 0.98::aRTCO2("HIGH") :- vENTALV("ZERO").
0.01::aRTCO2("LOW"); 0.01::aRTCO2("NORMAL"); 0.98::aRTCO2("HIGH") :- vENTALV("LOW").
0.04::aRTCO2("LOW"); 0.92::aRTCO2("NORMAL"); 0.04::aRTCO2("HIGH") :- vENTALV("NORMAL").
0.9::aRTCO2("LOW"); 0.09::aRTCO2("NORMAL"); 0.01::aRTCO2("HIGH") :- vENTALV("HIGH").
0.97::eXPCO2("ZERO"); 0.01::eXPCO2("LOW"); 0.01::eXPCO2("NORMAL"); 0.01::eXPCO2("HIGH") :- aRTCO2("LOW"), vENTLUNG("ZERO").
0.01::eXPCO2("ZERO"); 0.97::eXPCO2("LOW"); 0.01::eXPCO2("NORMAL"); 0.01::eXPCO2("HIGH") :- aRTCO2("LOW"), vENTLUNG("LOW").
0.01::eXPCO2("ZERO"); 0.01::eXPCO2("LOW"); 0.97::eXPCO2("NORMAL"); 0.01::eXPCO2("HIGH") :- aRTCO2("LOW"), vENTLUNG("NORMAL").
0.01::eXPCO2("ZERO"); 0.01::eXPCO2("LOW"); 0.01::eXPCO2("NORMAL"); 0.97::eXPCO2("HIGH") :- aRTCO2("LOW"), vENTLUNG("HIGH").
0.01::eXPCO2("ZERO"); 0.97::eXPCO2("LOW"); 0.01::eXPCO2("NORMAL"); 0.01::eXPCO2("HIGH") :- aRTCO2("NORMAL"), vENTLUNG("ZERO").
0.97::eXPCO2("ZERO"); 0.01::eXPCO2("LOW"); 0.01::eXPCO2("NORMAL"); 0.01::eXPCO2("HIGH") :- aRTCO2("NORMAL"), vENTLUNG("LOW").
0.01::eXPCO2("ZERO"); 0.01::eXPCO2("LOW"); 0.97::eXPCO2("NORMAL"); 0.01::eXPCO2("HIGH") :- aRTCO2("NORMAL"), vENTLUNG("NORMAL").
0.01::eXPCO2("ZERO"); 0.01::eXPCO2("LOW"); 0.01::eXPCO2("NORMAL"); 0.97::eXPCO2("HIGH") :- aRTCO2("NORMAL"), vENTLUNG("HIGH").
0.01::eXPCO2("ZERO"); 0.97::eXPCO2("LOW"); 0.01::eXPCO2("NORMAL"); 0.01::eXPCO2("HIGH") :- aRTCO2("HIGH"), vENTLUNG("ZERO").
0.01::eXPCO2("ZERO"); 0.01::eXPCO2("LOW"); 0.97::eXPCO2("NORMAL"); 0.01::eXPCO2("HIGH") :- aRTCO2("HIGH"), vENTLUNG("LOW").
0.97::eXPCO2("ZERO"); 0.01::eXPCO2("LOW"); 0.01::eXPCO2("NORMAL"); 0.01::eXPCO2("HIGH") :- aRTCO2("HIGH"), vENTLUNG("NORMAL").
0.01::eXPCO2("ZERO"); 0.01::eXPCO2("LOW"); 0.01::eXPCO2("NORMAL"); 0.97::eXPCO2("HIGH") :- aRTCO2("HIGH"), vENTLUNG("HIGH").
0.98::sAO2("LOW"); 0.01::sAO2("NORMAL"); 0.01::sAO2("HIGH") :- pVSAT("LOW"), sHUNT("NORMAL").
0.98::sAO2("LOW"); 0.01::sAO2("NORMAL"); 0.01::sAO2("HIGH") :- pVSAT("LOW"), sHUNT("HIGH").
0.01::sAO2("LOW"); 0.98::sAO2("NORMAL"); 0.01::sAO2("HIGH") :- pVSAT("NORMAL"), sHUNT("NORMAL").
0.98::sAO2("LOW"); 0.01::sAO2("NORMAL"); 0.01::sAO2("HIGH") :- pVSAT("NORMAL"), sHUNT("HIGH").
0.01::sAO2("LOW"); 0.01::sAO2("NORMAL"); 0.98::sAO2("HIGH") :- pVSAT("HIGH"), sHUNT("NORMAL").
0.69::sAO2("LOW"); 0.3::sAO2("NORMAL"); 0.01::sAO2("HIGH") :- pVSAT("HIGH"), sHUNT("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("LOW"), iNSUFFANESTH, sAO2("LOW"), tPR("LOW").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("LOW"), iNSUFFANESTH, sAO2("LOW"), tPR("NORMAL").
0.7::cATECHOL("NORMAL"); 0.3::cATECHOL("HIGH") :- aRTCO2("LOW"), iNSUFFANESTH, sAO2("LOW"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("LOW"), iNSUFFANESTH, sAO2("NORMAL"), tPR("LOW").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("LOW"), iNSUFFANESTH, sAO2("NORMAL"), tPR("NORMAL").
0.7::cATECHOL("NORMAL"); 0.3::cATECHOL("HIGH") :- aRTCO2("LOW"), iNSUFFANESTH, sAO2("NORMAL"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("LOW"), iNSUFFANESTH, sAO2("HIGH"), tPR("LOW").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("LOW"), iNSUFFANESTH, sAO2("HIGH"), tPR("NORMAL").
0.95::cATECHOL("NORMAL"); 0.05::cATECHOL("HIGH") :- aRTCO2("LOW"), iNSUFFANESTH, sAO2("HIGH"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("LOW"), \+iNSUFFANESTH, sAO2("LOW"), tPR("LOW").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("LOW"), \+iNSUFFANESTH, sAO2("LOW"), tPR("NORMAL").
0.7::cATECHOL("NORMAL"); 0.3::cATECHOL("HIGH") :- aRTCO2("LOW"), \+iNSUFFANESTH, sAO2("LOW"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("LOW"), \+iNSUFFANESTH, sAO2("NORMAL"), tPR("LOW").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("LOW"), \+iNSUFFANESTH, sAO2("NORMAL"), tPR("NORMAL").
0.95::cATECHOL("NORMAL"); 0.05::cATECHOL("HIGH") :- aRTCO2("LOW"), \+iNSUFFANESTH, sAO2("NORMAL"), tPR("HIGH").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("LOW"), \+iNSUFFANESTH, sAO2("HIGH"), tPR("LOW").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("LOW"), \+iNSUFFANESTH, sAO2("HIGH"), tPR("NORMAL").
0.95::cATECHOL("NORMAL"); 0.05::cATECHOL("HIGH") :- aRTCO2("LOW"), \+iNSUFFANESTH, sAO2("HIGH"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("NORMAL"), iNSUFFANESTH, sAO2("LOW"), tPR("LOW").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("NORMAL"), iNSUFFANESTH, sAO2("LOW"), tPR("NORMAL").
0.7::cATECHOL("NORMAL"); 0.3::cATECHOL("HIGH") :- aRTCO2("NORMAL"), iNSUFFANESTH, sAO2("LOW"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("NORMAL"), iNSUFFANESTH, sAO2("NORMAL"), tPR("LOW").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("NORMAL"), iNSUFFANESTH, sAO2("NORMAL"), tPR("NORMAL").
0.7::cATECHOL("NORMAL"); 0.3::cATECHOL("HIGH") :- aRTCO2("NORMAL"), iNSUFFANESTH, sAO2("NORMAL"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("NORMAL"), iNSUFFANESTH, sAO2("HIGH"), tPR("LOW").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("NORMAL"), iNSUFFANESTH, sAO2("HIGH"), tPR("NORMAL").
0.99::cATECHOL("NORMAL"); 0.01::cATECHOL("HIGH") :- aRTCO2("NORMAL"), iNSUFFANESTH, sAO2("HIGH"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("NORMAL"), \+iNSUFFANESTH, sAO2("LOW"), tPR("LOW").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("NORMAL"), \+iNSUFFANESTH, sAO2("LOW"), tPR("NORMAL").
0.7::cATECHOL("NORMAL"); 0.3::cATECHOL("HIGH") :- aRTCO2("NORMAL"), \+iNSUFFANESTH, sAO2("LOW"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("NORMAL"), \+iNSUFFANESTH, sAO2("NORMAL"), tPR("LOW").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("NORMAL"), \+iNSUFFANESTH, sAO2("NORMAL"), tPR("NORMAL").
0.99::cATECHOL("NORMAL"); 0.01::cATECHOL("HIGH") :- aRTCO2("NORMAL"), \+iNSUFFANESTH, sAO2("NORMAL"), tPR("HIGH").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("NORMAL"), \+iNSUFFANESTH, sAO2("HIGH"), tPR("LOW").
0.05::cATECHOL("NORMAL"); 0.95::cATECHOL("HIGH") :- aRTCO2("NORMAL"), \+iNSUFFANESTH, sAO2("HIGH"), tPR("NORMAL").
0.99::cATECHOL("NORMAL"); 0.01::cATECHOL("HIGH") :- aRTCO2("NORMAL"), \+iNSUFFANESTH, sAO2("HIGH"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), iNSUFFANESTH, sAO2("LOW"), tPR("LOW").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), iNSUFFANESTH, sAO2("LOW"), tPR("NORMAL").
0.1::cATECHOL("NORMAL"); 0.9::cATECHOL("HIGH") :- aRTCO2("HIGH"), iNSUFFANESTH, sAO2("LOW"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), iNSUFFANESTH, sAO2("NORMAL"), tPR("LOW").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), iNSUFFANESTH, sAO2("NORMAL"), tPR("NORMAL").
0.1::cATECHOL("NORMAL"); 0.9::cATECHOL("HIGH") :- aRTCO2("HIGH"), iNSUFFANESTH, sAO2("NORMAL"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), iNSUFFANESTH, sAO2("HIGH"), tPR("LOW").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), iNSUFFANESTH, sAO2("HIGH"), tPR("NORMAL").
0.3::cATECHOL("NORMAL"); 0.7::cATECHOL("HIGH") :- aRTCO2("HIGH"), iNSUFFANESTH, sAO2("HIGH"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), \+iNSUFFANESTH, sAO2("LOW"), tPR("LOW").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), \+iNSUFFANESTH, sAO2("LOW"), tPR("NORMAL").
0.1::cATECHOL("NORMAL"); 0.9::cATECHOL("HIGH") :- aRTCO2("HIGH"), \+iNSUFFANESTH, sAO2("LOW"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), \+iNSUFFANESTH, sAO2("NORMAL"), tPR("LOW").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), \+iNSUFFANESTH, sAO2("NORMAL"), tPR("NORMAL").
0.3::cATECHOL("NORMAL"); 0.7::cATECHOL("HIGH") :- aRTCO2("HIGH"), \+iNSUFFANESTH, sAO2("NORMAL"), tPR("HIGH").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), \+iNSUFFANESTH, sAO2("HIGH"), tPR("LOW").
0.01::cATECHOL("NORMAL"); 0.99::cATECHOL("HIGH") :- aRTCO2("HIGH"), \+iNSUFFANESTH, sAO2("HIGH"), tPR("NORMAL").
0.3::cATECHOL("NORMAL"); 0.7::cATECHOL("HIGH") :- aRTCO2("HIGH"), \+iNSUFFANESTH, sAO2("HIGH"), tPR("HIGH").
0.05::hR("LOW"); 0.9::hR("NORMAL"); 0.05::hR("HIGH") :- cATECHOL("NORMAL").
0.01::hR("LOW"); 0.09::hR("NORMAL"); 0.9::hR("HIGH") :- cATECHOL("HIGH").
0.98::hRBP("LOW"); 0.01::hRBP("NORMAL"); 0.01::hRBP("HIGH") :- eRRLOWOUTPUT, hR("LOW").
0.3::hRBP("LOW"); 0.4::hRBP("NORMAL"); 0.3::hRBP("HIGH") :- eRRLOWOUTPUT, hR("NORMAL").
0.01::hRBP("LOW"); 0.98::hRBP("NORMAL"); 0.01::hRBP("HIGH") :- eRRLOWOUTPUT, hR("HIGH").
0.4::hRBP("LOW"); 0.59::hRBP("NORMAL"); 0.01::hRBP("HIGH") :- \+eRRLOWOUTPUT, hR("LOW").
0.98::hRBP("LOW"); 0.01::hRBP("NORMAL"); 0.01::hRBP("HIGH") :- \+eRRLOWOUTPUT, hR("NORMAL").
0.01::hRBP("LOW"); 0.01::hRBP("NORMAL"); 0.98::hRBP("HIGH") :- \+eRRLOWOUTPUT, hR("HIGH").
0.98::cO("LOW"); 0.01::cO("NORMAL"); 0.01::cO("HIGH") :- hR("LOW"), sTROKEVOLUME("LOW").
0.95::cO("LOW"); 0.04::cO("NORMAL"); 0.01::cO("HIGH") :- hR("LOW"), sTROKEVOLUME("NORMAL").
0.3::cO("LOW"); 0.69::cO("NORMAL"); 0.01::cO("HIGH") :- hR("LOW"), sTROKEVOLUME("HIGH").
0.95::cO("LOW"); 0.04::cO("NORMAL"); 0.01::cO("HIGH") :- hR("NORMAL"), sTROKEVOLUME("LOW").
0.04::cO("LOW"); 0.95::cO("NORMAL"); 0.01::cO("HIGH") :- hR("NORMAL"), sTROKEVOLUME("NORMAL").
0.01::cO("LOW"); 0.3::cO("NORMAL"); 0.69::cO("HIGH") :- hR("NORMAL"), sTROKEVOLUME("HIGH").
0.8::cO("LOW"); 0.19::cO("NORMAL"); 0.01::cO("HIGH") :- hR("HIGH"), sTROKEVOLUME("LOW").
0.01::cO("LOW"); 0.04::cO("NORMAL"); 0.95::cO("HIGH") :- hR("HIGH"), sTROKEVOLUME("NORMAL").
0.01::cO("LOW"); 0.01::cO("NORMAL"); 0.98::cO("HIGH") :- hR("HIGH"), sTROKEVOLUME("HIGH").
0.3333333::hREKG("LOW"); 0.3333333::hREKG("NORMAL"); 0.3333333::hREKG("HIGH") :- eRRCAUTER, hR("LOW").
0.3333333::hREKG("LOW"); 0.3333333::hREKG("NORMAL"); 0.3333333::hREKG("HIGH") :- eRRCAUTER, hR("NORMAL").
0.01::hREKG("LOW"); 0.98::hREKG("NORMAL"); 0.01::hREKG("HIGH") :- eRRCAUTER, hR("HIGH").
0.3333333::hREKG("LOW"); 0.3333333::hREKG("NORMAL"); 0.3333333::hREKG("HIGH") :- \+eRRCAUTER, hR("LOW").
0.98::hREKG("LOW"); 0.01::hREKG("NORMAL"); 0.01::hREKG("HIGH") :- \+eRRCAUTER, hR("NORMAL").
0.01::hREKG("LOW"); 0.01::hREKG("NORMAL"); 0.98::hREKG("HIGH") :- \+eRRCAUTER, hR("HIGH").
0.3333333::hRSAT("LOW"); 0.3333333::hRSAT("NORMAL"); 0.3333333::hRSAT("HIGH") :- eRRCAUTER, hR("LOW").
0.3333333::hRSAT("LOW"); 0.3333333::hRSAT("NORMAL"); 0.3333333::hRSAT("HIGH") :- eRRCAUTER, hR("NORMAL").
0.01::hRSAT("LOW"); 0.98::hRSAT("NORMAL"); 0.01::hRSAT("HIGH") :- eRRCAUTER, hR("HIGH").
0.3333333::hRSAT("LOW"); 0.3333333::hRSAT("NORMAL"); 0.3333333::hRSAT("HIGH") :- \+eRRCAUTER, hR("LOW").
0.98::hRSAT("LOW"); 0.01::hRSAT("NORMAL"); 0.01::hRSAT("HIGH") :- \+eRRCAUTER, hR("NORMAL").
0.01::hRSAT("LOW"); 0.01::hRSAT("NORMAL"); 0.98::hRSAT("HIGH") :- \+eRRCAUTER, hR("HIGH").
0.98::bP("LOW"); 0.01::bP("NORMAL"); 0.01::bP("HIGH") :- cO("LOW"), tPR("LOW").
0.98::bP("LOW"); 0.01::bP("NORMAL"); 0.01::bP("HIGH") :- cO("LOW"), tPR("NORMAL").
0.3::bP("LOW"); 0.6::bP("NORMAL"); 0.1::bP("HIGH") :- cO("LOW"), tPR("HIGH").
0.98::bP("LOW"); 0.01::bP("NORMAL"); 0.01::bP("HIGH") :- cO("NORMAL"), tPR("LOW").
0.1::bP("LOW"); 0.85::bP("NORMAL"); 0.05::bP("HIGH") :- cO("NORMAL"), tPR("NORMAL").
0.05::bP("LOW"); 0.4::bP("NORMAL"); 0.55::bP("HIGH") :- cO("NORMAL"), tPR("HIGH").
0.9::bP("LOW"); 0.09::bP("NORMAL"); 0.01::bP("HIGH") :- cO("HIGH"), tPR("LOW").
0.05::bP("LOW"); 0.2::bP("NORMAL"); 0.75::bP("HIGH") :- cO("HIGH"), tPR("NORMAL").
0.01::bP("LOW"); 0.09::bP("NORMAL"); 0.9::bP("HIGH") :- cO("HIGH"), tPR("HIGH").
query(cO("HIGH")).