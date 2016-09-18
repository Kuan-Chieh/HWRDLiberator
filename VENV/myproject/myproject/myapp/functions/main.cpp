//
//  main.cpp
//  bomparser
//
//  Created by Wendi Cheng on 2014/8/23.
//  Copyright (c) 2014¦~ ___Wendi Cheng___. All rights reserved.
//

#include <iostream>
#include <fstream>
#include <vector>
#include <math.h>
#include <stdlib.h>
#include <cstring>

const int page_row = 44;
const int page_clm = 83;
const int PN_Index = 5;
const int PN_Max = 27;
const int Qty_Index = 40;
const int Qty_Max	= 51;
const int Loc_Index = 61;
const int Loc_Max = 81;
const int Desp_Index = 5;
const int Desp_Max = 80;
const int sPN_Index = 4;

using namespace std;


class Part{
	vector<string> PartNumber;
	vector<string> Locations;
	string Desp;
	int item_qty;
    
public:
	Part(){
		item_qty = 0;
		Desp.clear();
		PartNumber.clear();
		Locations.clear();
	};
    
	string location(int index){
		return Locations[index];
	}
	string main_source(){
		return PartNumber[0];
	}
	
	bool have_2nd();
	string sourcePN(int index){
		return PartNumber[index];
	}
	
	int PN_count(){
		int cc=0;
		for(vector<string>::iterator ss = PartNumber.begin(); ss != PartNumber.end();ss++)
			cc++;
		return cc;
	}
	
	int Location_count(){
		int cc=0;
		for(vector<string>::iterator ss = Locations.begin(); ss != Locations.end();ss++)
			cc++;
		return cc;
	}
	
	void add_PN(string ss){
		PartNumber.push_back(ss);
	}
	
	void add_Location(string ss){
		Locations.push_back(ss);
	}
	
	void set_Desp(string ss){
		Desp = ss;
	}
	
	void set_Qty(int q){
		item_qty = q;
	}
	
	string get_Desp(){
		return Desp;
	}
	
	int get_Qty(){
		return item_qty;
	}
};

class Parser{
	ifstream BOM;
	ofstream target;
	char **page;
	int s_row;
	int e_row;
    int page_size;
    int item_count;
    Part tmp;
    vector<Part> wBOM;
    
	int item_srow();	//return new item start row
	string get_main();	//return main source PN
	string get_second();	//return
	int get_qty();
	void get_location();
	bool open_BOM(char *filename);
	bool open_BOM(string filename);
	bool next_item();	//get next item into Part
	void add_Location(int row, int end_row, int Qty, Part *pp);
	void get_2ndPN(int ss, int ee);
	//int next_page();	//import page into page[][]
	void skip_line(int ll){
		string dl;
		for(int i=0;i<ll && !BOM.eof();i++)
			getline(BOM, dl);
	};
	
    int get_item_row(int ss){
        for (int i=ss; i<page_size; i++)
            if(page[i][3] == '0')
                return i;
        return page_size;
    }
    
    string get_string(int row, int ss, int ee){
		string tmp;
		for(int i=ss;i<ee;i++)
			tmp.push_back(page[row][i]);
		
		return tmp;
	}
	
	string cut_PN(string ss){
		string tmp;
		
		int i=0;
		while(ss[i] != ' '){
			tmp.push_back(ss[i]);
			i++;
		}
		return tmp;
	}
	
	string cut_Desp(string ss){
		int i = ss.length()-1;
		string tmp;
		while(ss[i] == ' '){
			i--;
		}
		for(int j=0;j<=i;j++)
			tmp.push_back(ss[j]);
			
		return tmp;
	}
	
	int sQty2Qty(string ss){	//string Qty to int Qty
		char *ct = new char[ss.length()];
		
		std::strcpy (ct, ss.c_str());
		
		return (int)atoi(ct);
	}
    
	void print_page(){
		for(int i=0;i<page_size;i++){
			for(int j=0;j<page_clm;j++){
				cout<<page[i][j];
			}
			cout<<endl;
		}
	}
    
	void page_init(int rr){
		for(int i=0;i<rr;i++)
			for(int j=0;j<page_clm;j++)
				page[i][j] = ' ';
	}
	
	void output_wBOM(char* out){
		ofstream CSV(out);
		
		for(vector<Part>::iterator sp = wBOM.begin(); sp != wBOM.end(); sp++){
			//main source PN
			CSV<<(*sp).main_source()<<'\t';
			
			//Locations
			int qq = (*sp).Location_count();
			for(int x=0; x<qq; x++){
				CSV<<(*sp).location(x)<<','<<' ';
			}
			CSV<<'\t';
			
						
			//Description
			CSV<<(*sp).get_Desp()<<'\t';
			
			int pqq = (*sp).PN_count();
			for(int x=1;x<pqq;x++){
				CSV<<(*sp).sourcePN(x)<<'\t';
			}
			CSV<<endl;
		}
	}
	
	void output_wBOM_1(char* out){
		ofstream outBOM(out);
		
		for(vector<Part>::iterator sp = wBOM.begin(); sp != wBOM.end(); sp++){
			outBOM<<(*sp).main_source()<<'\t';
			outBOM<<(*sp).get_Desp()<<endl;
			
			int qq = (*sp).Location_count();
			for(int x=0; x<qq; x++){
				if(x == qq-1)
					outBOM<<(*sp).location(x);
				else
					outBOM<<(*sp).location(x)<<'|';
			}
			outBOM<<endl;
		}
	}
    
public:
	Parser(){
		s_row = 0;
		e_row = 0;
        page_size = 0;
        item_count = 0;
	};

	bool parse(int fc, char** filename);
};

bool Parser::parse(int fc, char** filename){
	page_size =0;
	int tfc = 1;
	string tmpBOM = "temp_BOM.txt";
	
	target.open(tmpBOM.c_str());
		
		string ss;
		for(;tfc<fc-1;tfc++){
			if(!open_BOM(filename[tfc])){
				cout<<"Cannot open file \""<<filename[tfc]<<"\""<<endl;
				return false;
			}
			
			while(!BOM.eof()){
				skip_line(12);
				if(!BOM.eof()){
					for(int i=0;i<page_row && !BOM.eof();i++){
						getline(BOM,ss);
						if(ss.empty())
							continue;
						target<<ss<<endl;
						page_size++;
					}
				}
				skip_line(4);
				skip_line(6);
			}
		BOM.close();
		}
		
		target.close();
		
		if(open_BOM(tmpBOM)){
			page = new char*[page_size];
			for(int i=0;i<page_size;i++)
				page[i] = new char[page_clm];
				
			
			page_init(page_size);
			for(int i=0;i<page_size && (!BOM.eof());i++){
				ss.clear();
				getline(BOM, ss);
				for(int j=0;j<page_clm && j<ss.length();j++){
            		page[i][j] = ss[j];
				}
			}
		
			while(next_item()){
				//cout<<"*******************************************"<<endl;
			}
		}
		
		output_wBOM(filename[tfc]);
		cout<<"BOM parsering OK!"<<endl;
		cout<<"output BOM file : "<<filename[tfc]<<endl;
	return true;
}

bool Parser::open_BOM(char *file_name){
	BOM.open(file_name);

	return BOM.is_open();
}

bool Parser::open_BOM(string file_name){
	BOM.open(file_name.c_str());

	return BOM.is_open();
}


void Parser::add_Location(int row, int end_row, int Qty, Part *pp){
	string tmp="", tloc;
	
	do{
		tmp.clear();
		tmp = get_string(row, Loc_Index, Loc_Max);
		tloc.clear();
		for(int i=0;i<tmp.length() && Qty>0;i++){
			if(tmp[i]==','){
				Qty--;
				(*pp).add_Location(tloc);
				//cout<<tloc<<endl;
				tloc.clear();
				continue;
			}
			if(tmp[i]==' '){
				break;
			}
			tloc.push_back(tmp[i]);
			//cout<<tmp[i]<<endl;
		}
		row++;
		if(row == end_row)
			return;
	}while(Qty>0);
}

void Parser::get_2ndPN(int ss, int ee){
	
	for(int i=ss;i<ee;i++){
		if(page[i][sPN_Index] == '('){
			cout<<" - "<<cut_PN(get_string(i, PN_Index, PN_Max))<<endl;
		}
	}
	
}

bool Parser::next_item(){
    string sQty;
    int Qty;
    Part ptmp;
    
	s_row = get_item_row(s_row);
    e_row = get_item_row(s_row+1);
    
    if(s_row == e_row)
    	return false;

	
	string spn = cut_PN(get_string(s_row, PN_Index, PN_Max));
	if(spn[0] == '6' && spn[1] == '0')
		return false;
	
	ptmp.add_PN(spn);
	//cout<<"PN : "<<cut_PN(get_string(s_row, PN_Index, PN_Max))<<endl;
	//get_2ndPN(s_row, e_row);
	for(int i=s_row;i<e_row;i++){
		if(page[i][sPN_Index] == '('){
			ptmp.add_PN(cut_PN(get_string(i, PN_Index, PN_Max)));
			//cout<<"2nd Source : "<<endl;
			//cout<<" - "<<cut_PN(get_string(i, PN_Index, PN_Max))<<endl;
		}
	}
	
	ptmp.set_Desp(cut_Desp(get_string(s_row+1, Desp_Index, Desp_Max)));
	//cout<<"Desp : "<<cut_Desp(get_string(s_row+1, Desp_Index, Desp_Max))<<endl;
	
	sQty = get_string(s_row, Qty_Index, Qty_Max);
	Qty = sQty2Qty(sQty);
	ptmp.set_Qty(Qty);
	//cout<<"Qty : "<<Qty<<endl;
 
	add_Location(s_row+2, e_row, Qty, &ptmp);
	
	wBOM.push_back(ptmp);
    
    s_row = e_row;
    
    return true;
}


int main(int argc, char *argv[]){
    
	Parser BB;

	char *ss[] = {"0","70.TXT", "tttt.txt"};
	
//	if(argc > 1)
		//BB.parse(argc, argv);
		BB.parse(3, ss);
	//else
	//	cout<<"miss BOM file"<<endl;
	system("PAUSE");
    
	return 0;
}


