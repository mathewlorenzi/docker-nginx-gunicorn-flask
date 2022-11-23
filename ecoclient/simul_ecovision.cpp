//#include "HTTPRequest.hpp"

// g++ ./simul_ecovision.cpp -o ./simul_ecovision
// OK http but KO https not handled
// OK ./simul_ecovision --url http://127.0.0.1:5000 --method GET --camId UNKNOWN
// KO https:  ./simul_ecovision --url https://www.ecovision.ovh:81 --camId polo

// OK: https://gist.github.com/alghanmi/c5d7b761b2c9ab199157
// OK g++ ./simul_ecovision.cpp -o ./simul_ecovision -lcurl
// ./simul_ecovision --url http://127.0.0.1:5000 --camId paula7
// fedora
//  OK: sudo dnf install libcurl*   => libcurl-minimal installed and others
//  no tested fedora https://pkgs.org/download/libcurl-openssl

// OK curl -X GET https://www.ecovision.ovh:81/last_image_filename/polo


// g++ ./simul_ecovision.cpp ./base64.cpp -o ./simul_ecovision -lcurl
// ./simul_ecovision --url http://127.0.0.1:5000 --camId paulo9

//#include <iostream>
//#include <fstream>
//#include "HTTPRequest.hpp"
//#include <unistd.h>
//#include <fstream> // for strema log

#include "curl_request.h"
#include "raw_to_png.h"

//app.py part of the flask servre
// OK
/*@app.route("/image", methods=["GET"])
def image():
   filename = os.path.join(get_test_dir(get_root_dir()), "data", "verysmall.jpg")
   with open( filename, mode="rb" ) as f:
       imageContent = f.read()#.decode("iso-8859-1")
       return imageContent*/
// KO
/*from detecteur_black_template.api.v1.routes.utils import get_test_dir
@app.route("/image", methods=["GET"])
def image() -> str:
   filename = os.path.join(get_test_dir(get_root_dir()), "data", "verysmall.jpg")
   with open( filename, mode="rb" ) as f:
       imageContent = f.read().decode("iso-8859-1")
       #(open(input_filename, "rb").read()).decode("iso-8859-1")
       dict_out = {
           "timestamp": "TODO_or_willbeinfilename",
           "filename": "small.jpg",
           "stream": imageContent
       }
       return dict_out
*/
  
// optional
//#include <typeinfo>
  
// for int mkdir(const char *pathname, mode_t mode); 
//#include <sys/stat.h> 
//#include <sys/types.h> 
  
  
int main(int argc, const char* argv[])
{
    std::string filename = "temp_raw_to_png.png";
    int width = 256;
    int height = 256;
    int bitdepth = 8;
    int pitch = 3*width;
    int colortype = PNG_COLOR_TYPE_RGB;
    unsigned char* data = new unsigned char[width*height*3];
    int counter = 0;
    for(int row=0; row<height; row++){
        for(int col=0; col<width; col++){
            std::cout << row << " " << col << " " << counter << std::endl;
            int R=row, G=0, B=0;
            // if(row<1){B=255;}
            data[counter] = (unsigned char)(R); counter++;
            data[counter] = (unsigned char)(G); counter++;
            data[counter] = (unsigned char)(B); counter++;
        }
    }


    /*for(int row=0; row<height; row++){
        for(int col=0; col<width; col++){
            int val = 0;
            if(row==height/2 && col==width/2){val=255;}
            data[counter] = (unsigned char)(val); counter++;
        }
    }
    for(int row=0; row<height; row++){
        for(int col=0; col<width; col++){
            int val = 255;
            if(row==height/2 && col==width/2){val=255;}
            data[counter] = (unsigned char)(val); counter++;
        }
    }
    for(int row=0; row<height; row++){
        for(int col=0; col<width; col++){
            int val = 0;
            if(row==height/2 && col==width/2){val=255;}
            data[counter] = (unsigned char)(val); counter++;
        }
    }*/


    std::cout << width*height << std::endl;
    int ret = save_png(filename,
                     width, height, bitdepth, colortype,
                     data, pitch);
    std::cout << "ret: " << ret << std::endl;
    return ret;
    
    /*CurlGetRequester curler;
    //std::string _url = "https://www.ecovision.ovh:81"
    std::string _url = "http://127.0.0.1:5000";
    curler.get(_url+"/last_image_filename/polo", true);
    curler.get(_url+"/last_image_filename/polo", true);
    curler.get(_url+"/last_image_filename/pola", true);
    curler.get("https://www.ecovision.ovh:80", true);
    curler.get(_url+"/last_image_filename/polo", true);
    curler.get(_url+"/last_image_filename/polo", true);
    return 0;*/

    bool debug = true;

    //std::string whatToSend = "message";
    std::string whatToSend = "image";

    std::string uri = "";
    std::string camId = "";
    for (int i = 1; i < argc; ++i)
    {
        const auto arg = std::string{argv[i]};
        if (arg == "--help"){
            std::cout << "[INFO]example ./simul_ecovision --url http://127.0.0.1:5000 --camId UNKNOWN\n";
            return EXIT_SUCCESS;
        }
        else if (arg == "--url"){
            if (++i < argc) uri = argv[i];
            else throw std::runtime_error("[ERROR]Missing argument for --url");
        }
        else if (arg == "--camId"){
            if (++i < argc) camId = argv[i];
            else throw std::runtime_error("[ERROR]Missing argument for --camId");
        }
        else
            throw std::runtime_error{"[ERROR]Invalid flag: " + arg};
    }
    
    httpRequestUtils reqPost;
    httpRequestUtils reqGet;
    unsigned int waitIntervalBeforeRetrying = 3;
    unsigned int waitTotal = 13;    
    bool printRequestDetails = true;
    std::string _msg;
    std::string tempDirForLastCurrentImage = "./output_simulecovision";
    if(reqGet.initialise_for_get(uri, camId, tempDirForLastCurrentImage, waitIntervalBeforeRetrying, waitTotal, printRequestDetails, _msg)==false){
        std::cout << _msg << std::endl;
        return 1;
    }
    if(reqPost.initialise_for_post(uri, camId, waitIntervalBeforeRetrying, waitTotal, printRequestDetails, _msg)==false){
        std::cout << _msg << std::endl;
        return 1;
    }

    int waitToGrabNextImage = 5;
    while(true)
    {
        std::string outputSavedImage;
        bool succHttpRequestGet = reqGet.getRequestImage(outputSavedImage, _msg);
        if(succHttpRequestGet==false){
            std::cout << "[ERROR]simul_ecovision failed get: " << _msg << std::endl;
            return EXIT_FAILURE;
        }
        //std::string todentMessage = "hello im the post message";
        //if(outputSavedImage != "" && debug==true){
        //    std::cout << "[DEBUG]Image ready to be processed: " << outputSavedImage << std::endl;
        //}

        std::string jsonObjStr;
        if(whatToSend == "message")
        {
            jsonObjStr += "{";
            jsonObjStr += " \"nbtracks\" : " + std::to_string(4) + ",";
            jsonObjStr += " \"type\" : \"tblr\", ";
            jsonObjStr += " \"1\" : [10, 10, 50, 50], ";
            jsonObjStr += " \"2\" : [100, 150, 100, 150], ";
            jsonObjStr += " \"3\" : [20, 50, 150, 50], ";
            jsonObjStr += " \"4\" : [70, 20, 60, 90] ";
            jsonObjStr += " }";
        }
        else if(whatToSend == "image")
        {
            // std::ifstream fim("input.png");
            //with open("input.png", mode="rb") as fim:
            //    content = base64_encode(data, false);
            //    jsonObjStr = content

                /*data = base64.encodebytes(data)
                return jsonify({'msg': 'success', 'size': [img.width, img.height], 'img': data})      
                for jpeg:
                <img src="data:image/jpeg;base64,...base64 data...">
                for png:
                <img src="data:image/png;base64,...base64 data...">*/


            /*std::ifstream file;
            size_t size = 0;

            file.open("input.png", std::ios::in | std::ios::binary);
            char* data = 0;

            file.seekg(0, std::ios::end);
            size = file.tellg();
            std::cout << "File size: " << size << std::endl;
            file.seekg(0, std::ios::beg);

            data = new char[size - 8 + 1];
            file.seekg(8); // skip the header
            file.read(data, size - 8);
            data[size] = '\0';
            std::cout << "Data size: " << file.tellg() << std::endl;
            // cin.get();
            
            jsonObjStr = data;*/

            std::ifstream fin("input.png", std::ios::in | std::ios::binary);
            std::ostringstream oss;
            oss << fin.rdbuf();
            //std::string data(oss.str());
            //jsonObjStr = oss.str();
            // OK: jsonObjStr = base64_encode(oss.str(), false);

            //std::cout << "[INFO]data: " << data << std::endl;
            //std::cout << "[INFO]jsonObjStr: " << jsonObjStr << std::endl;
            //getchar();


            jsonObjStr += "{";
            jsonObjStr += " \"nbtracks\" : " + std::to_string(4) + ",";
            jsonObjStr += " \"type\" : \"tblr\", ";
            jsonObjStr += " \"png\" : \"" + base64_encode(oss.str(), false) + "\",";
            jsonObjStr += " \"1\" : [10, 10, 50, 50], ";
            jsonObjStr += " \"2\" : [100, 150, 100, 150], ";
            jsonObjStr += " \"3\" : [20, 50, 150, 50], ";
            jsonObjStr += " \"4\" : [70, 20, 60, 90] ";
            jsonObjStr += " }";

        }
        else
        {
            std::cout << "[ERROR]what to send wrong" << std::endl;
        }

        bool succHttpRequestPost = reqPost.postRequestJsonMessage(jsonObjStr, _msg);
        if(succHttpRequestPost==false){
            std::cout << "[ERROR]simul_ecovision failed: " << _msg << std::endl;
            return EXIT_FAILURE;
        }
        
        if(debug==true){std::cout << _msg << std::endl;}
        std::cout << "[INFO]Success Post Request: " << _msg << std::endl;
        
        unsigned int microseconds = waitToGrabNextImage*1000000;
        if(debug==true){
            std::cout << "[DEBUG]Sleep for: " << microseconds/1000000 << '\n';
        }
        usleep(microseconds);
    }

    return EXIT_SUCCESS;
}