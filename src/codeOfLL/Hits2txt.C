{
   gROOT->Reset();
   TFile f("optical.root");

   //TTree *Coincidences = (TTree*)gDirectory->Get("Coincidences");
   TTree *Hits = (TTree*)gDirectory->Get("Hits");
   std::ofstream out("Hits.txt");
//cout<<"jeje"<<endl;
   //TTree *Singles = (TTree*)gDirectory->Get("Singles");
   //TTree *delay = (TTree*)gDirectory->Get("delay";

//
//Declaration of leaves types - TTree Coincidences
//  
   



   Int_t           runID;
   Int_t           trackID;
   Int_t           photonID;
   Int_t           eventID;
   Int_t           nCompton;
   Int_t           particalID;
   Char_t          proName[30];
   Float_t         globalPosX;
   Float_t         globalPosY;  
   Float_t         globalPosZ;
   Float_t         energy;
   Float_t         sourcePosX;
   Float_t         sourcePosY;
   Float_t         sourcePosZ;
   Float_t         momX;
   Float_t         momY;
   Float_t         momZ;
//   Float_t         dirx;
//   Float_t         diry;
//   Float_t         dirz;

   

//   
//Set branch addresses - TTree Hits
// 
   Hits->SetBranchAddress("edep", &energy);
   Hits->SetBranchAddress("trackID", &trackID);
   Hits->SetBranchAddress("runID", &runID);
   Hits->SetBranchAddress("photonID", &photonID);
   Hits->SetBranchAddress("eventID", &eventID);
   Hits->SetBranchAddress("posX", &globalPosX);
   Hits->SetBranchAddress("posY", &globalPosY);
   Hits->SetBranchAddress("posZ", &globalPosZ);
   Hits->SetBranchAddress("sourcePosX", &sourcePosX);
   Hits->SetBranchAddress("sourcePosY", &sourcePosY);
   Hits->SetBranchAddress("sourcePosZ", &sourcePosZ);
   Hits->SetBranchAddress("momDirX", &momX);
   Hits->SetBranchAddress("momDirY", &momY);
   Hits->SetBranchAddress("momDirZ", &momZ);
   Hits->SetBranchAddress("nCrystalCompton", &nCompton);
   Hits->SetBranchAddress("processName", &proName);
   Hits->SetBranchAddress("PDGEncoding", &particalID);
   Hits->SetBranchAddress("localPosX", &localPosX);
   Hits->SetBranchAddress("localPosY", &localPosY);
   Hits->SetBranchAddress("localPosZ", &localPosZ);

   Int_t nentries = Hits->GetEntries();
   Int_t nbytes = 0;

//
// Loop for each event in the TTree Coincidences
//
   out << "runID,eventID,photonID,trackID,processName,x,y,z,srcX,srcY,srcZ,dirx,diry,dirz,momX,momY,momZ,energy,nCompton,particalID" << std::endl; 
   for (Int_t i=0; i<nentries;i++) {
      nbytes += Hits->GetEntry(i);
      out<<runID<<","<<eventID<<","<<photonID<<","<<trackID<<","<<proName<<","<<globalPosX<<","<<globalPosY<<","<<globalPosZ<<","<<sourcePosX<<","<<sourcePosY<<","<<sourcePosZ<<","<<dirx<<","<<diry<<","<<dirz<<","<<momX<<","<<momY<<","<<momZ<<","<<energy<<","<<nCompton<<","<<partical<<std::endl;
   }
   out.close();
   
}	
