%% ProbLog program: PGM 51
%% Created on 2024-03-30 00:25:08.913914
query(propCost("Million")).
0.1::mileage("FiveThou"); 0.4::mileage("TwentyThou"); 0.4::mileage("FiftyThou"); 0.1::mileage("Domino").
0.2::age("Adolescent"); 0.6::age("Adult"); 0.2::age("Senior").
0.5::socioEcon("Prole"); 0.2::socioEcon("Middle"); 0.29::socioEcon("UpperMiddle"); 0.01::socioEcon("Wealthy") :- age("Senior").
0.4::socioEcon("Prole"); 0.4::socioEcon("Middle"); 0.19::socioEcon("UpperMiddle"); 0.01::socioEcon("Wealthy") :- \+age("Senior").
0.01::riskAversion("Psychopath"); 0.04::riskAversion("Adventurous"); 0.35::riskAversion("Normal"); 0.6::riskAversion("Cautious") :- age("Senior"), socioEcon("Middle").
0.01::riskAversion("Psychopath"); 0.09::riskAversion("Adventurous"); 0.4::riskAversion("Normal"); 0.5::riskAversion("Cautious") :- age("Senior"), \+socioEcon("Middle").
0.015::riskAversion("Psychopath"); 0.285::riskAversion("Adventurous"); 0.4::riskAversion("Normal"); 0.3::riskAversion("Cautious") :- age("Adult"), socioEcon("Wealthy").
0.015::riskAversion("Psychopath"); 0.185::riskAversion("Adventurous"); 0.6::riskAversion("Normal"); 0.2::riskAversion("Cautious") :- age("Adult"), socioEcon("Middle").
0.015::riskAversion("Psychopath"); 0.285::riskAversion("Adventurous"); 0.5::riskAversion("Normal"); 0.2::riskAversion("Cautious") :- age("Adult"), (socioEcon("Prole"); socioEcon("UpperMiddle")).
0.02::riskAversion("Psychopath"); 0.48::riskAversion("Adventurous"); 0.4::riskAversion("Normal"); 0.1::riskAversion("Cautious") :- age("Adolescent"), socioEcon("UpperMiddle").
0.02::riskAversion("Psychopath"); 0.38::riskAversion("Adventurous"); 0.5::riskAversion("Normal"); 0.1::riskAversion("Cautious") :- age("Adolescent"), socioEcon("Middle").
0.02::riskAversion("Psychopath"); 0.58::riskAversion("Adventurous"); 0.3::riskAversion("Normal"); 0.1::riskAversion("Cautious") :- age("Adolescent"), (socioEcon("Prole"); socioEcon("Wealthy")).
0.5::otherCar :- socioEcon("Prole").
0.8::otherCar :- socioEcon("Middle").
0.9::otherCar :- socioEcon("UpperMiddle").
0.95::otherCar :- socioEcon("Wealthy").
\+goodStudent :- age("Senior").
\+goodStudent :- age("Adult").
0.1::goodStudent :- socioEcon("Prole"), age("Adolescent").
0.2::goodStudent :- socioEcon("Middle"), age("Adolescent").
0.5::goodStudent :- socioEcon("UpperMiddle"), age("Adolescent").
0.4::goodStudent :- socioEcon("Wealthy"), age("Adolescent").
0.3::makeModel("SportsCar"); 0.01::makeModel("Economy"); 0.09::makeModel("FamilySedan"); 0.4::makeModel("Luxury"); 0.2::makeModel("SuperLuxury") :- socioEcon("Wealthy").
0.2::makeModel("SportsCar"); 0.05::makeModel("Economy"); 0.3::makeModel("FamilySedan"); 0.45::makeModel("Luxury") :- socioEcon("UpperMiddle").
0.15::makeModel("SportsCar"); 0.2::makeModel("Economy"); 0.65::makeModel("FamilySedan") :- socioEcon("Middle").
0.1::makeModel("SportsCar"); 0.7::makeModel("Economy"); 0.2::makeModel("FamilySedan") :- socioEcon("Prole").
0.9::seniorTrain :- age("Senior"), riskAversion("Cautious").
0.3::seniorTrain :- age("Senior"), riskAversion("Normal").
1e-06::seniorTrain :- age("Senior"), (riskAversion("Adventurous"); riskAversion("Psychopath")).
\+seniorTrain :- age("Adult").
\+seniorTrain :- age("Adolescent").
0.999999::antiTheft :- riskAversion("Cautious"), \+socioEcon("Prole").
0.95::antiTheft :- riskAversion("Cautious"), socioEcon("Prole").
0.1::antiTheft :- riskAversion("Normal"), socioEcon("Prole").
0.3::antiTheft :- riskAversion("Normal"), socioEcon("Middle").
0.9::antiTheft :- riskAversion("Normal"), socioEcon("UpperMiddle").
0.8::antiTheft :- riskAversion("Normal"), socioEcon("Wealthy").
0.5::antiTheft :- riskAversion("Adventurous"), socioEcon("Wealthy").
0.2::antiTheft :- riskAversion("Adventurous"), socioEcon("UpperMiddle").
1e-06::antiTheft :- riskAversion("Adventurous"), (socioEcon("Prole"); socioEcon("Middle")).
0.5::antiTheft :- riskAversion("Psychopath"), socioEcon("Wealthy").
0.05::antiTheft :- riskAversion("Psychopath"), socioEcon("UpperMiddle").
1e-06::antiTheft :- riskAversion("Psychopath"), (socioEcon("Prole"); socioEcon("Middle")).
0.1::vehicleYear :- socioEcon("Wealthy").
0.2::vehicleYear :- socioEcon("UpperMiddle").
0.7::vehicleYear :- socioEcon("Middle").
0.85::vehicleYear :- socioEcon("Prole").
0.489999::homeBase("Secure"); 0.5::homeBase("City"); 1e-06::homeBase("Suburb"); 0.01::homeBase("Rural") :- riskAversion("Psychopath"), socioEcon("Wealthy").
0.95::homeBase("Secure"); 1e-06::homeBase("City"); 1e-06::homeBase("Suburb"); 0.049998::homeBase("Rural") :- riskAversion("Adventurous"), socioEcon("Wealthy").
0.85::homeBase("Secure"); 1e-06::homeBase("City"); 0.001::homeBase("Suburb"); 0.148999::homeBase("Rural") :- riskAversion("Normal"), socioEcon("Wealthy").
0.999997::homeBase("Secure"); 1e-06::homeBase("City"); 1e-06::homeBase("Suburb"); 1e-06::homeBase("Rural") :- riskAversion("Cautious"), socioEcon("Wealthy").
0.35::homeBase("Secure"); 0.6::homeBase("City"); 0.04::homeBase("Suburb"); 0.01::homeBase("Rural") :- riskAversion("Psychopath"), socioEcon("UpperMiddle").
0.2::homeBase("Secure"); 0.4::homeBase("City"); 0.3::homeBase("Suburb"); 0.1::homeBase("Rural") :- riskAversion("Adventurous"), socioEcon("UpperMiddle").
0.5::homeBase("Secure"); 1e-06::homeBase("City"); 0.4::homeBase("Suburb"); 0.099999::homeBase("Rural") :- riskAversion("Normal"), socioEcon("UpperMiddle").
0.999997::homeBase("Secure"); 1e-06::homeBase("City"); 1e-06::homeBase("Suburb"); 1e-06::homeBase("Rural") :- riskAversion("Cautious"), socioEcon("UpperMiddle").
0.15::homeBase("Secure"); 0.8::homeBase("City"); 0.04::homeBase("Suburb"); 0.01::homeBase("Rural") :- riskAversion("Psychopath"), socioEcon("Middle").
0.01::homeBase("Secure"); 0.25::homeBase("City"); 0.6::homeBase("Suburb"); 0.14::homeBase("Rural") :- riskAversion("Adventurous"), socioEcon("Middle").
0.299999::homeBase("Secure"); 1e-06::homeBase("City"); 0.6::homeBase("Suburb"); 0.1::homeBase("Rural") :- riskAversion("Normal"), socioEcon("Middle").
0.95::homeBase("Secure"); 1e-06::homeBase("City"); 0.024445::homeBase("Suburb"); 0.025554::homeBase("Rural") :- riskAversion("Cautious"), socioEcon("Middle").
1e-06::homeBase("Secure"); 0.8::homeBase("City"); 0.05::homeBase("Suburb"); 0.149999::homeBase("Rural") :- \+riskAversion("Psychopath"), socioEcon("Prole").
1e-06::homeBase("Secure"); 0.8::homeBase("City"); 0.049999::homeBase("Suburb"); 0.15::homeBase("Rural") :- riskAversion("Psychopath"), socioEcon("Prole").
0.6::airbag :- makeModel("Luxury"), vehicleYear.
0.2::airbag :- makeModel("FamilySedan"), vehicleYear.
0.05::airbag :- makeModel("Economy"), vehicleYear.
0.1::airbag :- (makeModel("SportsCar"); makeModel("SuperLuxury")), vehicleYear.
airbag :- \+vehicleYear.
0.1::drivingSkill("SubStandard"); 0.6::drivingSkill("Normal"); 0.3::drivingSkill("Expert") :- age("Senior"), seniorTrain.
0.4::drivingSkill("SubStandard"); 0.5::drivingSkill("Normal"); 0.1::drivingSkill("Expert") :- age("Senior"), \+seniorTrain.
0.3::drivingSkill("SubStandard"); 0.6::drivingSkill("Normal"); 0.1::drivingSkill("Expert") :- age("Adult").
0.5::drivingSkill("SubStandard"); 0.45::drivingSkill("Normal"); 0.05::drivingSkill("Expert") :- age("Adolescent").
0.15::antilock :- makeModel("SuperLuxury"), vehicleYear.
0.3::antilock :- makeModel("Luxury"), vehicleYear.
\+antilock :- (makeModel("FamilySedan"); makeModel("Economy")), vehicleYear.
0.1::antilock :- makeModel("SportsCar"), vehicleYear.
0.99::antilock :- (makeModel("Luxury"); makeModel("SuperLuxury")), \+vehicleYear.
0.4::antilock :- makeModel("FamilySedan"), \+vehicleYear.
0.001::antilock :- makeModel("Economy"), \+vehicleYear.
0.9::antilock :- makeModel("SportsCar"), \+vehicleYear.
0.05::ruggedAuto("EggShell"); 0.55::ruggedAuto("Football"); 0.4::ruggedAuto("Tank") :- makeModel("SuperLuxury").
0.1::ruggedAuto("EggShell"); 0.6::ruggedAuto("Football"); 0.3::ruggedAuto("Tank") :- makeModel("Luxury").
0.2::ruggedAuto("EggShell"); 0.6::ruggedAuto("Football"); 0.2::ruggedAuto("Tank") :- makeModel("FamilySedan"), \+vehicleYear.
0.05::ruggedAuto("EggShell"); 0.55::ruggedAuto("Football"); 0.4::ruggedAuto("Tank") :- makeModel("FamilySedan"), vehicleYear.
0.5::ruggedAuto("EggShell"); 0.5::ruggedAuto("Football") :- makeModel("Economy"), \+vehicleYear.
0.9::ruggedAuto("EggShell"); 0.1::ruggedAuto("Football") :- makeModel("Economy"), vehicleYear.
0.95::ruggedAuto("EggShell"); 0.04::ruggedAuto("Football"); 0.01::ruggedAuto("Tank") :- makeModel("SportsCar").
1e-06::carValue("FiveThou"); 1e-06::carValue("TenThou"); 1e-06::carValue("TwentyThou"); 1e-06::carValue("FiftyThou"); 0.999996::carValue("Million") :- makeModel("SuperLuxury"), vehicleYear.
0.01::carValue("FiveThou"); 0.09::carValue("TenThou"); 0.2::carValue("TwentyThou"); 0.7::carValue("FiftyThou") :- makeModel("Luxury"), vehicleYear, mileage("FiveThou").
0.05::carValue("FiveThou"); 0.15::carValue("TenThou"); 0.3::carValue("TwentyThou"); 0.5::carValue("FiftyThou") :- makeModel("Luxury"), vehicleYear, mileage("TwentyThou").
0.1::carValue("FiveThou"); 0.3::carValue("TenThou"); 0.3::carValue("TwentyThou"); 0.3::carValue("FiftyThou") :- makeModel("Luxury"), vehicleYear, mileage("FiftyThou").
0.2::carValue("FiveThou"); 0.2::carValue("TenThou"); 0.3::carValue("TwentyThou"); 0.3::carValue("FiftyThou") :- makeModel("Luxury"), vehicleYear, mileage("Domino").
0.2::carValue("FiveThou"); 0.3::carValue("TenThou"); 0.5::carValue("TwentyThou") :- makeModel("FamilySedan"), vehicleYear, mileage("FiveThou").
0.5::carValue("FiveThou"); 0.3::carValue("TenThou"); 0.2::carValue("TwentyThou") :- makeModel("FamilySedan"), vehicleYear, mileage("TwentyThou").
0.7::carValue("FiveThou"); 0.2::carValue("TenThou"); 0.1::carValue("TwentyThou") :- makeModel("FamilySedan"), vehicleYear, mileage("FiftyThou").
0.99::carValue("FiveThou"); 0.009999::carValue("TenThou"); 1e-06::carValue("TwentyThou") :- makeModel("FamilySedan"), vehicleYear, mileage("Domino").
0.25::carValue("FiveThou"); 0.7::carValue("TenThou"); 0.05::carValue("TwentyThou") :- makeModel("Economy"), vehicleYear, mileage("FiveThou").
0.7::carValue("FiveThou"); 0.2999::carValue("TenThou"); 0.0001::carValue("TwentyThou") :- makeModel("Economy"), vehicleYear, mileage("TwentyThou").
0.99::carValue("FiveThou"); 0.009999::carValue("TenThou"); 1e-06::carValue("TwentyThou") :- makeModel("Economy"), vehicleYear, mileage("FiftyThou").
0.999998::carValue("FiveThou"); 1e-06::carValue("TenThou"); 1e-06::carValue("TwentyThou") :- makeModel("Economy"), vehicleYear, mileage("Domino").
0.03::carValue("FiveThou"); 0.3::carValue("TenThou"); 0.6::carValue("TwentyThou"); 0.06::carValue("FiftyThou"); 0.01::carValue("Million") :- makeModel("SportsCar"), vehicleYear, mileage("FiveThou").
0.16::carValue("FiveThou"); 0.5::carValue("TenThou"); 0.3::carValue("TwentyThou"); 0.03::carValue("FiftyThou"); 0.01::carValue("Million") :- makeModel("SportsCar"), vehicleYear, mileage("TwentyThou").
0.4::carValue("FiveThou"); 0.47::carValue("TenThou"); 0.1::carValue("TwentyThou"); 0.02::carValue("FiftyThou"); 0.01::carValue("Million") :- makeModel("SportsCar"), vehicleYear, mileage("FiftyThou").
0.9::carValue("FiveThou"); 0.06::carValue("TenThou"); 0.02::carValue("TwentyThou"); 0.01::carValue("FiftyThou"); 0.01::carValue("Million") :- makeModel("SportsCar"), vehicleYear, mileage("Domino").
carValue("Million") :- makeModel("SuperLuxury"), \+vehicleYear.
carValue("FiftyThou") :- makeModel("Luxury"), \+vehicleYear.
0.1::carValue("TenThou"); 0.9::carValue("TwentyThou") :- makeModel("FamilySedan"), \+vehicleYear.
0.1::carValue("FiveThou"); 0.8::carValue("TenThou"); 0.1::carValue("TwentyThou") :- makeModel("Economy"), \+vehicleYear.
0.1::carValue("TenThou"); 0.8::carValue("TwentyThou"); 0.09::carValue("FiftyThou"); 0.01::carValue("Million") :- makeModel("SportsCar"), \+vehicleYear.
drivQuality("Excellent") :- drivingSkill("Expert"), (riskAversion("Normal"); riskAversion("Cautious")).
0.01::drivQuality("Poor"); 0.01::drivQuality("Normal"); 0.98::drivQuality("Excellent") :- drivingSkill("Expert"), riskAversion("Adventurous").
0.3::drivQuality("Poor"); 0.2::drivQuality("Normal"); 0.5::drivQuality("Excellent") :- drivingSkill("Expert"), riskAversion("Psychopath").
0.5::drivQuality("Poor"); 0.2::drivQuality("Normal"); 0.3::drivQuality("Excellent") :- drivingSkill("Normal"), riskAversion("Psychopath").
0.3::drivQuality("Poor"); 0.4::drivQuality("Normal"); 0.3::drivQuality("Excellent") :- drivingSkill("Normal"), riskAversion("Adventurous").
drivQuality("Normal") :- drivingSkill("Normal"), riskAversion("Normal").
0.8::drivQuality("Normal"); 0.2::drivQuality("Excellent") :- drivingSkill("Normal"), riskAversion("Cautious").
drivQuality("Poor") :- drivingSkill("SubStandard").
0.3::drivHist("Zero"); 0.3::drivHist("One"); 0.4::drivHist("Many") :- drivingSkill("SubStandard"), riskAversion("Cautious").
0.95::drivHist("Zero"); 0.04::drivHist("One"); 0.01::drivHist("Many") :- drivingSkill("Normal"), riskAversion("Cautious").
0.999998::drivHist("Zero"); 1e-06::drivHist("One"); 1e-06::drivHist("Many") :- drivingSkill("Expert"), riskAversion("Cautious").
0.03::drivHist("Zero"); 0.15::drivHist("One"); 0.82::drivHist("Many") :- drivingSkill("SubStandard"), riskAversion("Normal").
0.9::drivHist("Zero"); 0.07::drivHist("One"); 0.03::drivHist("Many") :- drivingSkill("Normal"), riskAversion("Normal").
0.99::drivHist("Zero"); 0.009999::drivHist("One"); 1e-06::drivHist("Many") :- drivingSkill("Expert"), riskAversion("Normal").
0.002::drivHist("Zero"); 0.008::drivHist("One"); 0.99::drivHist("Many") :- drivingSkill("SubStandard"), riskAversion("Adventurous").
0.5::drivHist("Zero"); 0.3::drivHist("One"); 0.2::drivHist("Many") :- drivingSkill("Normal"), riskAversion("Adventurous").
0.6::drivHist("Zero"); 0.3::drivHist("One"); 0.1::drivHist("Many") :- drivingSkill("Expert"), riskAversion("Adventurous").
0.001::drivHist("Zero"); 0.004::drivHist("One"); 0.995::drivHist("Many") :- drivingSkill("SubStandard"), riskAversion("Psychopath").
0.1::drivHist("Zero"); 0.3::drivHist("One"); 0.6::drivHist("Many") :- drivingSkill("Normal"), riskAversion("Psychopath").
0.3::drivHist("Zero"); 0.3::drivHist("One"); 0.4::drivHist("Many") :- drivingSkill("Expert"), riskAversion("Psychopath").
0.5::cushioning("Poor"); 0.3::cushioning("Fair"); 0.2::cushioning("Good") :- ruggedAuto("EggShell"), airbag.
0.7::cushioning("Poor"); 0.3::cushioning("Fair") :- ruggedAuto("EggShell"), \+airbag.
0.1::cushioning("Fair"); 0.6::cushioning("Good"); 0.3::cushioning("Excellent") :- ruggedAuto("Football"), airbag.
0.1::cushioning("Poor"); 0.6::cushioning("Fair"); 0.3::cushioning("Good") :- ruggedAuto("Football"), \+airbag.
cushioning("Excellent") :- ruggedAuto("Tank"), airbag.
0.7::cushioning("Good"); 0.3::cushioning("Excellent") :- ruggedAuto("Tank"), \+airbag.
1e-06::theft :- carValue("Million").
5e-05::theft :- antiTheft, homeBase("Rural"), carValue("FiftyThou").
0.0002::theft :- \+antiTheft, homeBase("Rural"), carValue("FiftyThou").
0.0003::theft :- antiTheft, homeBase("Suburb"), carValue("FiftyThou").
0.0005::theft :- \+antiTheft, homeBase("Suburb"), carValue("FiftyThou").
0.005::theft :- antiTheft, homeBase("City"), carValue("FiftyThou").
0.01::theft :- \+antiTheft, homeBase("City"), carValue("FiftyThou").
2e-06::theft :- homeBase("Secure"), carValue("FiftyThou").
5e-05::theft :- antiTheft, homeBase("Rural"), carValue("TwentyThou").
0.0002::theft :- \+antiTheft, homeBase("Rural"), carValue("TwentyThou").
0.0003::theft :- antiTheft, homeBase("Suburb"), carValue("TwentyThou").
0.0005::theft :- \+antiTheft, homeBase("Suburb"), carValue("TwentyThou").
0.005::theft :- antiTheft, homeBase("City"), carValue("TwentyThou").
0.01::theft :- \+antiTheft, homeBase("City"), carValue("TwentyThou").
3e-06::theft :- homeBase("Secure"), carValue("TwentyThou").
2e-05::theft :- antiTheft, homeBase("Rural"), carValue("TenThou").
0.0001::theft :- \+antiTheft, homeBase("Rural"), carValue("TenThou").
0.0001::theft :- antiTheft, homeBase("Suburb"), carValue("TenThou").
0.0002::theft :- \+antiTheft, homeBase("Suburb"), carValue("TenThou").
0.002::theft :- antiTheft, homeBase("City"), carValue("TenThou").
0.005::theft :- \+antiTheft, homeBase("City"), carValue("TenThou").
2e-06::theft :- homeBase("Secure"), carValue("TenThou").
1e-05::theft :- homeBase("Rural"), carValue("FiveThou").
1e-05::theft :- homeBase("Suburb"), carValue("FiveThou").
0.0005::theft :- antiTheft, homeBase("City"), carValue("FiveThou").
0.001::theft :- \+antiTheft, homeBase("City"), carValue("FiveThou").
1e-06::theft :- homeBase("Secure"), carValue("FiveThou").
0.985::accident("None"); 0.01::accident("Mild"); 0.003::accident("Moderate"); 0.002::accident("Severe") :- antilock, mileage("Domino"), drivQuality("Excellent").
0.98::accident("None"); 0.01::accident("Mild"); 0.007::accident("Moderate"); 0.003::accident("Severe") :- \+antilock, mileage("Domino"), drivQuality("Excellent").
0.99::accident("None"); 0.007::accident("Mild"); 0.002::accident("Moderate"); 0.001::accident("Severe") :- antilock, mileage("FiftyThou"), drivQuality("Excellent").
0.98::accident("None"); 0.01::accident("Mild"); 0.005::accident("Moderate"); 0.005::accident("Severe") :- \+antilock, mileage("FiftyThou"), drivQuality("Excellent").
0.995::accident("None"); 0.003::accident("Mild"); 0.001::accident("Moderate"); 0.001::accident("Severe") :- antilock, mileage("TwentyThou"), drivQuality("Excellent").
0.99::accident("None"); 0.007::accident("Mild"); 0.002::accident("Moderate"); 0.001::accident("Severe") :- \+antilock, mileage("TwentyThou"), drivQuality("Excellent").
0.999::accident("None"); 0.0007::accident("Mild"); 0.0002::accident("Moderate"); 0.0001::accident("Severe") :- antilock, mileage("FiveThou"), drivQuality("Excellent").
0.995::accident("None"); 0.003::accident("Mild"); 0.001::accident("Moderate"); 0.001::accident("Severe") :- \+antilock, mileage("FiveThou"), drivQuality("Excellent").
0.95::accident("None"); 0.03::accident("Mild"); 0.01::accident("Moderate"); 0.01::accident("Severe") :- antilock, mileage("Domino"), drivQuality("Normal").
0.94::accident("None"); 0.03::accident("Mild"); 0.02::accident("Moderate"); 0.01::accident("Severe") :- \+antilock, mileage("Domino"), drivQuality("Normal").
0.97::accident("None"); 0.02::accident("Mild"); 0.007::accident("Moderate"); 0.003::accident("Severe") :- antilock, mileage("FiftyThou"), drivQuality("Normal").
0.95::accident("None"); 0.03::accident("Mild"); 0.015::accident("Moderate"); 0.005::accident("Severe") :- \+antilock, mileage("FiftyThou"), drivQuality("Normal").
0.98::accident("None"); 0.01::accident("Mild"); 0.005::accident("Moderate"); 0.005::accident("Severe") :- antilock, mileage("TwentyThou"), drivQuality("Normal").
0.96::accident("None"); 0.02::accident("Mild"); 0.015::accident("Moderate"); 0.005::accident("Severe") :- \+antilock, mileage("TwentyThou"), drivQuality("Normal").
0.99::accident("None"); 0.007::accident("Mild"); 0.002::accident("Moderate"); 0.001::accident("Severe") :- antilock, mileage("FiveThou"), drivQuality("Normal").
0.98::accident("None"); 0.01::accident("Mild"); 0.005::accident("Moderate"); 0.005::accident("Severe") :- \+antilock, mileage("FiveThou"), drivQuality("Normal").
0.7::accident("None"); 0.2::accident("Mild"); 0.07::accident("Moderate"); 0.03::accident("Severe") :- antilock, mileage("FiveThou"), drivQuality("Poor").
0.4::accident("None"); 0.3::accident("Mild"); 0.2::accident("Moderate"); 0.1::accident("Severe") :- antilock, mileage("TwentyThou"), drivQuality("Poor").
0.3::accident("None"); 0.3::accident("Mild"); 0.2::accident("Moderate"); 0.2::accident("Severe") :- antilock, mileage("FiftyThou"), drivQuality("Poor").
0.2::accident("None"); 0.2::accident("Mild"); 0.3::accident("Moderate"); 0.3::accident("Severe") :- antilock, mileage("Domino"), drivQuality("Poor").
0.6::accident("None"); 0.2::accident("Mild"); 0.1::accident("Moderate"); 0.1::accident("Severe") :- \+antilock, mileage("FiveThou"), drivQuality("Poor").
0.3::accident("None"); 0.2::accident("Mild"); 0.2::accident("Moderate"); 0.3::accident("Severe") :- \+antilock, mileage("TwentyThou"), drivQuality("Poor").
0.2::accident("None"); 0.2::accident("Mild"); 0.2::accident("Moderate"); 0.4::accident("Severe") :- \+antilock, mileage("FiftyThou"), drivQuality("Poor").
0.1::accident("None"); 0.1::accident("Mild"); 0.3::accident("Moderate"); 0.5::accident("Severe") :- \+antilock, mileage("Domino"), drivQuality("Poor").
0.9::medCost("Thousand"); 0.05::medCost("TenThou"); 0.03::medCost("HundredThou"); 0.02::medCost("Million") :- accident("Severe"), age("Senior"), cushioning("Excellent").
0.95::medCost("Thousand"); 0.03::medCost("TenThou"); 0.01::medCost("HundredThou"); 0.01::medCost("Million") :- accident("Severe"), \+age("Senior"), cushioning("Excellent").
0.6::medCost("Thousand"); 0.3::medCost("TenThou"); 0.07::medCost("HundredThou"); 0.03::medCost("Million") :- accident("Severe"), age("Senior"), cushioning("Good").
0.9::medCost("Thousand"); 0.07::medCost("TenThou"); 0.02::medCost("HundredThou"); 0.01::medCost("Million") :- accident("Severe"), \+age("Senior"), cushioning("Good").
0.3::medCost("Thousand"); 0.3::medCost("TenThou"); 0.2::medCost("HundredThou"); 0.2::medCost("Million") :- accident("Severe"), age("Senior"), cushioning("Fair").
0.5::medCost("Thousand"); 0.2::medCost("TenThou"); 0.2::medCost("HundredThou"); 0.1::medCost("Million") :- accident("Severe"), \+age("Senior"), cushioning("Fair").
0.2::medCost("Thousand"); 0.2::medCost("TenThou"); 0.3::medCost("HundredThou"); 0.3::medCost("Million") :- accident("Severe"), age("Senior"), cushioning("Poor").
0.3::medCost("Thousand"); 0.3::medCost("TenThou"); 0.2::medCost("HundredThou"); 0.2::medCost("Million") :- accident("Severe"), \+age("Senior"), cushioning("Poor").
0.95::medCost("Thousand"); 0.03::medCost("TenThou"); 0.01::medCost("HundredThou"); 0.01::medCost("Million") :- accident("Moderate"), age("Senior"), cushioning("Excellent").
0.99::medCost("Thousand"); 0.007::medCost("TenThou"); 0.002::medCost("HundredThou"); 0.001::medCost("Million") :- accident("Moderate"), \+age("Senior"), cushioning("Excellent").
0.9::medCost("Thousand"); 0.07::medCost("TenThou"); 0.02::medCost("HundredThou"); 0.01::medCost("Million") :- accident("Moderate"), age("Senior"), cushioning("Good").
0.95::medCost("Thousand"); 0.02::medCost("TenThou"); 0.02::medCost("HundredThou"); 0.01::medCost("Million") :- accident("Moderate"), \+age("Senior"), cushioning("Good").
0.5::medCost("Thousand"); 0.2::medCost("TenThou"); 0.2::medCost("HundredThou"); 0.1::medCost("Million") :- accident("Moderate"), age("Senior"), cushioning("Fair").
0.8::medCost("Thousand"); 0.15::medCost("TenThou"); 0.03::medCost("HundredThou"); 0.02::medCost("Million") :- accident("Moderate"), \+age("Senior"), cushioning("Fair").
0.3::medCost("Thousand"); 0.3::medCost("TenThou"); 0.2::medCost("HundredThou"); 0.2::medCost("Million") :- accident("Moderate"), age("Senior"), cushioning("Poor").
0.5::medCost("Thousand"); 0.2::medCost("TenThou"); 0.2::medCost("HundredThou"); 0.1::medCost("Million") :- accident("Moderate"), \+age("Senior"), cushioning("Poor").
0.99::medCost("Thousand"); 0.007::medCost("TenThou"); 0.002::medCost("HundredThou"); 0.001::medCost("Million") :- accident("Mild"), age("Senior"), cushioning("Excellent").
0.999::medCost("Thousand"); 0.00099::medCost("TenThou"); 9e-06::medCost("HundredThou"); 1e-06::medCost("Million") :- accident("Mild"), \+age("Senior"), cushioning("Excellent").
0.97::medCost("Thousand"); 0.025::medCost("TenThou"); 0.003::medCost("HundredThou"); 0.002::medCost("Million") :- accident("Mild"), age("Senior"), cushioning("Good").
0.99::medCost("Thousand"); 0.0099::medCost("TenThou"); 9e-05::medCost("HundredThou"); 1e-05::medCost("Million") :- accident("Mild"), \+age("Senior"), cushioning("Good").
0.95::medCost("Thousand"); 0.04::medCost("TenThou"); 0.007::medCost("HundredThou"); 0.003::medCost("Million") :- accident("Mild"), age("Senior"), cushioning("Fair").
0.98::medCost("Thousand"); 0.019::medCost("TenThou"); 0.0009::medCost("HundredThou"); 0.0001::medCost("Million") :- accident("Mild"), \+age("Senior"), cushioning("Fair").
0.9::medCost("Thousand"); 0.07::medCost("TenThou"); 0.02::medCost("HundredThou"); 0.01::medCost("Million") :- accident("Mild"), age("Senior"), cushioning("Poor").
0.96::medCost("Thousand"); 0.03::medCost("TenThou"); 0.009::medCost("HundredThou"); 0.001::medCost("Million") :- accident("Mild"), \+age("Senior"), cushioning("Poor").
medCost("Thousand") :- accident("None").
0.2::otherCarCost("Thousand"); 0.4::otherCarCost("TenThou"); 0.39996::otherCarCost("HundredThou"); 4e-05::otherCarCost("Million") :- accident("Severe"), ruggedAuto("EggShell").
0.1::otherCarCost("Thousand"); 0.5::otherCarCost("TenThou"); 0.39994::otherCarCost("HundredThou"); 6e-05::otherCarCost("Million") :- accident("Severe"), ruggedAuto("Football").
0.005::otherCarCost("Thousand"); 0.55::otherCarCost("TenThou"); 0.4449::otherCarCost("HundredThou"); 0.0001::otherCarCost("Million") :- accident("Severe"), ruggedAuto("Tank").
0.6::otherCarCost("Thousand"); 0.2::otherCarCost("TenThou"); 0.19998::otherCarCost("HundredThou"); 2e-05::otherCarCost("Million") :- accident("Moderate"), ruggedAuto("EggShell").
0.5::otherCarCost("Thousand"); 0.2::otherCarCost("TenThou"); 0.29997::otherCarCost("HundredThou"); 3e-05::otherCarCost("Million") :- accident("Moderate"), ruggedAuto("Football").
0.4::otherCarCost("Thousand"); 0.3::otherCarCost("TenThou"); 0.29996::otherCarCost("HundredThou"); 4e-05::otherCarCost("Million") :- accident("Moderate"), ruggedAuto("Tank").
0.99::otherCarCost("Thousand"); 0.005::otherCarCost("TenThou"); 0.00499::otherCarCost("HundredThou"); 1e-05::otherCarCost("Million") :- accident("Mild"), ruggedAuto("EggShell").
0.9799657::otherCarCost("Thousand"); 0.00999965::otherCarCost("TenThou"); 0.009984651::otherCarCost("HundredThou"); 4.999825e-05::otherCarCost("Million") :- accident("Mild"), ruggedAuto("Football").
0.95::otherCarCost("Thousand"); 0.03::otherCarCost("TenThou"); 0.01998::otherCarCost("HundredThou"); 2e-05::otherCarCost("Million") :- accident("Mild"), ruggedAuto("Tank").
otherCarCost("Thousand") :- accident("None").
1e-06::thisCarDam("None"); 9e-06::thisCarDam("Mild"); 9e-05::thisCarDam("Moderate"); 0.9999::thisCarDam("Severe") :- accident("Severe"), ruggedAuto("EggShell").
1e-06::thisCarDam("None"); 0.000999::thisCarDam("Mild"); 0.009::thisCarDam("Moderate"); 0.99::thisCarDam("Severe") :- accident("Severe"), ruggedAuto("Football").
0.05::thisCarDam("None"); 0.2::thisCarDam("Mild"); 0.2::thisCarDam("Moderate"); 0.55::thisCarDam("Severe") :- accident("Severe"), ruggedAuto("Tank").
1e-06::thisCarDam("None"); 0.000999::thisCarDam("Mild"); 0.7::thisCarDam("Moderate"); 0.299::thisCarDam("Severe") :- accident("Moderate"), ruggedAuto("EggShell").
0.001::thisCarDam("None"); 0.099::thisCarDam("Mild"); 0.8::thisCarDam("Moderate"); 0.1::thisCarDam("Severe") :- accident("Moderate"), ruggedAuto("Football").
0.05::thisCarDam("None"); 0.6::thisCarDam("Mild"); 0.3::thisCarDam("Moderate"); 0.05::thisCarDam("Severe") :- accident("Moderate"), ruggedAuto("Tank").
0.001::thisCarDam("None"); 0.9::thisCarDam("Mild"); 0.098::thisCarDam("Moderate"); 0.001::thisCarDam("Severe") :- accident("Mild"), ruggedAuto("EggShell").
0.2::thisCarDam("None"); 0.75::thisCarDam("Mild"); 0.049999::thisCarDam("Moderate"); 1e-06::thisCarDam("Severe") :- accident("Mild"), ruggedAuto("Football").
0.7::thisCarDam("None"); 0.29::thisCarDam("Mild"); 0.009999::thisCarDam("Moderate"); 1e-06::thisCarDam("Severe") :- accident("Mild"), ruggedAuto("Tank").
thisCarDam("None") :- accident("None").
iLiCost("Thousand") :- accident("None").
0.999::iLiCost("Thousand"); 0.000998::iLiCost("TenThou"); 1e-06::iLiCost("HundredThou"); 1e-06::iLiCost("Million") :- accident("Mild").
0.9::iLiCost("Thousand"); 0.05::iLiCost("TenThou"); 0.03::iLiCost("HundredThou"); 0.02::iLiCost("Million") :- accident("Moderate").
0.8::iLiCost("Thousand"); 0.1::iLiCost("TenThou"); 0.06::iLiCost("HundredThou"); 0.04::iLiCost("Million") :- accident("Severe").
0.05::thisCarCost("Thousand"); 0.95::thisCarCost("TenThou") :- thisCarDam("Severe"), carValue("FiveThou"), \+theft.
0.01::thisCarCost("Thousand"); 0.99::thisCarCost("TenThou") :- thisCarDam("Severe"), carValue("TenThou"), \+theft.
0.005::thisCarCost("Thousand"); 0.005::thisCarCost("TenThou"); 0.99::thisCarCost("HundredThou") :- thisCarDam("Severe"), carValue("TwentyThou"), \+theft.
0.001::thisCarCost("Thousand"); 0.001::thisCarCost("TenThou"); 0.998::thisCarCost("HundredThou") :- thisCarDam("Severe"), carValue("FiftyThou"), \+theft.
1e-06::thisCarCost("Thousand"); 1e-06::thisCarCost("TenThou"); 0.029998::thisCarCost("HundredThou"); 0.97::thisCarCost("Million") :- thisCarDam("Severe"), carValue("Million"), \+theft.
1e-06::thisCarCost("Thousand"); 1e-06::thisCarCost("TenThou"); 0.009998::thisCarCost("HundredThou"); 0.99::thisCarCost("Million") :- thisCarDam("Severe"), carValue("Million"), theft.
1e-06::thisCarCost("Thousand"); 1e-06::thisCarCost("TenThou"); 0.999998::thisCarCost("HundredThou") :- thisCarDam("Severe"), (carValue("TwentyThou"); carValue("FiftyThou")), theft.
1e-06::thisCarCost("Thousand"); 0.999999::thisCarCost("TenThou") :- thisCarDam("Severe"), carValue("TenThou"), theft.
0.03::thisCarCost("Thousand"); 0.97::thisCarCost("TenThou") :- thisCarDam("Severe"), carValue("FiveThou"), theft.
0.25::thisCarCost("Thousand"); 0.75::thisCarCost("TenThou") :- thisCarDam("Moderate"), carValue("FiveThou"), \+theft.
0.15::thisCarCost("Thousand"); 0.85::thisCarCost("TenThou") :- thisCarDam("Moderate"), carValue("TenThou"), \+theft.
0.01::thisCarCost("Thousand"); 0.01::thisCarCost("TenThou"); 0.98::thisCarCost("HundredThou") :- thisCarDam("Moderate"), carValue("TwentyThou"), \+theft.
0.005::thisCarCost("Thousand"); 0.005::thisCarCost("TenThou"); 0.99::thisCarCost("HundredThou") :- thisCarDam("Moderate"), carValue("FiftyThou"), \+theft.
0.003::thisCarCost("Thousand"); 0.003::thisCarCost("TenThou"); 0.044::thisCarCost("HundredThou"); 0.95::thisCarCost("Million") :- thisCarDam("Moderate"), carValue("Million"), \+theft.
0.001::thisCarCost("Thousand"); 0.001::thisCarCost("TenThou"); 0.018::thisCarCost("HundredThou"); 0.98::thisCarCost("Million") :- thisCarDam("Moderate"), carValue("Million"), theft.
0.001::thisCarCost("Thousand"); 0.001::thisCarCost("TenThou"); 0.998::thisCarCost("HundredThou") :- thisCarDam("Moderate"), (carValue("TwentyThou"); carValue("FiftyThou")), theft.
0.01::thisCarCost("Thousand"); 0.99::thisCarCost("TenThou") :- thisCarDam("Moderate"), carValue("TenThou"), theft.
0.05::thisCarCost("Thousand"); 0.95::thisCarCost("TenThou") :- thisCarDam("Moderate"), carValue("FiveThou"), theft.
0.98::thisCarCost("Thousand"); 0.01::thisCarCost("TenThou"); 0.01::thisCarCost("HundredThou") :- thisCarDam("Mild"), carValue("Million"), \+theft.
0.99::thisCarCost("Thousand"); 0.01::thisCarCost("TenThou") :- thisCarDam("Mild"), (carValue("TwentyThou"); carValue("FiftyThou")), \+theft.
0.95::thisCarCost("Thousand"); 0.05::thisCarCost("TenThou") :- thisCarDam("Mild"), (carValue("FiveThou"); carValue("TenThou")), \+theft.
0.02::thisCarCost("Thousand"); 0.03::thisCarCost("TenThou"); 0.25::thisCarCost("HundredThou"); 0.7::thisCarCost("Million") :- thisCarDam("Mild"), carValue("Million"), theft.
0.03::thisCarCost("Thousand"); 0.02::thisCarCost("TenThou"); 0.95::thisCarCost("HundredThou") :- thisCarDam("Mild"), (carValue("TwentyThou"); carValue("FiftyThou")), theft.
0.03::thisCarCost("Thousand"); 0.97::thisCarCost("TenThou") :- thisCarDam("Mild"), carValue("TenThou"), theft.
0.15::thisCarCost("Thousand"); 0.85::thisCarCost("TenThou") :- thisCarDam("Mild"), carValue("FiveThou"), theft.
thisCarCost("Thousand") :- thisCarDam("None"), \+theft.
0.04::thisCarCost("Thousand"); 0.01::thisCarCost("TenThou"); 0.2::thisCarCost("HundredThou"); 0.75::thisCarCost("Million") :- thisCarDam("None"), carValue("Million"), theft.
0.04::thisCarCost("Thousand"); 0.01::thisCarCost("TenThou"); 0.95::thisCarCost("HundredThou") :- thisCarDam("None"), (carValue("TwentyThou"); carValue("FiftyThou")), theft.
0.05::thisCarCost("Thousand"); 0.95::thisCarCost("TenThou") :- thisCarDam("None"), carValue("TenThou"), theft.
0.2::thisCarCost("Thousand"); 0.8::thisCarCost("TenThou") :- thisCarDam("None"), carValue("FiveThou"), theft.
propCost("Million") :- otherCarCost("Million").
0.98::propCost("HundredThou"); 0.02::propCost("Million") :- otherCarCost("HundredThou"), thisCarCost("Thousand").
0.8::propCost("HundredThou"); 0.2::propCost("Million") :- otherCarCost("HundredThou"), thisCarCost("TenThou").
0.6::propCost("HundredThou"); 0.4::propCost("Million") :- otherCarCost("HundredThou"), thisCarCost("HundredThou").
propCost("Million") :- otherCarCost("HundredThou"), thisCarCost("Million").
0.95::propCost("TenThou"); 0.05::propCost("HundredThou") :- otherCarCost("TenThou"), thisCarCost("Thousand").
0.6::propCost("TenThou"); 0.4::propCost("HundredThou") :- otherCarCost("TenThou"), thisCarCost("TenThou").
0.95::propCost("HundredThou"); 0.05::propCost("Million") :- otherCarCost("TenThou"), thisCarCost("HundredThou").
propCost("Million") :- otherCarCost("TenThou"), thisCarCost("Million").
0.7::propCost("Thousand"); 0.3::propCost("TenThou") :- otherCarCost("Thousand"), thisCarCost("Thousand").
0.95::propCost("TenThou"); 0.05::propCost("HundredThou") :- otherCarCost("Thousand"), thisCarCost("TenThou").
0.98::propCost("HundredThou"); 0.02::propCost("Million") :- otherCarCost("Thousand"), thisCarCost("HundredThou").
propCost("Million") :- otherCarCost("Thousand"), thisCarCost("Million").
