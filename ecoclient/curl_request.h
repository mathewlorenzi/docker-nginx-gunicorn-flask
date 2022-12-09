#include <cctype>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <algorithm>
#include <array>
#include <chrono>
#include <functional>
#include <map>
#include <memory>
#include <stdexcept>
#include <string>
#include <system_error>
#include <type_traits>
#include <vector>

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

//eco
#include <sys/time.h>
#include <iostream> // std::cout
#include <sys/stat.h> // for int mkdir(const char *pathname, mode_t mode); 
#include <sys/types.h> // for int mkdir(const char *pathname, mode_t mode); 
#include <fstream> // to save image as binary
   
#include <curl/curl.h>

#include "json.hpp"
 using json = nlohmann::json;

// convert tool on fedora: sudo dnf install ImageMagick

// https://github.com/ReneNyffenegger/cpp-base64
#include "base64.h"

struct WriteThis {
    const char *readptr;
    size_t sizeleft;
};

static size_t read_callback(char *dest, size_t size, size_t nmemb, void *userp)
{
  struct WriteThis *wt = (struct WriteThis *)userp;
  size_t buffer_size = size*nmemb;
 
  if(wt->sizeleft) {
    /* copy as much as possible from the source to the destination */
    size_t copy_this_much = wt->sizeleft;
    if(copy_this_much > buffer_size)
      copy_this_much = buffer_size;
    memcpy(dest, wt->readptr, copy_this_much);
 
    wt->readptr += copy_this_much;
    wt->sizeleft -= copy_this_much;
    return copy_this_much; /* we copied this many bytes */
  }
 
  return 0; /* no more data left to deliver */
}

static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

// https://curl.se/libcurl/c/post-callback.html
class CurlPostRequester
{
public:
    std::string outputMsg;
    bool debug = false;
    long http_code;
    /* silly test data to POST */
    //std::string data="Lorem ipsum dolor sit amet, consectetur adipiscing ";
    //"elit. Sed vel urna neque. Ut quis leo metus. Quisque eleifend, ex at " +
    //"laoreet rhoncus, odio ipsum semper metus, at tempus ante urna in mauris. " +
    //"Suspendisse ornare tempor venenatis. Ut dui neque, pellentesque a varius " +
    //"eget, mattis vitae ligula. Fusce ut pharetra est. Ut ullamcorper mi ac " +
    //"sollicitudin semper. Praesent sit amet tellus varius, posuere nulla non, " +
    //"rhoncus ipsum.";
    
    bool post_json(std::string url, std::string jsonObjStr)
    {
        outputMsg="[ERROR]CurlPostRequester empty out message";
        http_code = 0;
        CURL *curl;
        CURLcode res;

        if(debug==true)
        {
            std::cout << " =================== " << std::endl;
        }

        curl_global_init(CURL_GLOBAL_ALL);
        curl = curl_easy_init();
        if (curl == NULL) {
            outputMsg = std::string("[ERROR]CurlPostRequester libcurl init fct failed: code 128");
            if(debug==true){
                std::cout << outputMsg << std::endl;
            }
            return false;
        }

        /*char* jsonObj = "{ \"name\" : \"Pedro\", \"age\" : \"22\" }";
        //std::string jsonObjStr = "{ \"name\" : \"Pedro\" , \"age\" : \"22\" }";
        std::string jsonObjStr = "{";
        jsonObjStr += " \"name\" : \"Pedro\",";
        jsonObjStr += " \"age\" : \"22\"";
        jsonObjStr += " }";*/

        /*std::string jsonObjStr = "{";
        jsonObjStr += " \"nb\" : " + std::to_string(4) + ",";
        jsonObjStr += " \"type\" : \"tblr\", ";
        jsonObjStr += " \"1\" : [1, 2, 3, 4], ";
        jsonObjStr += " \"2\" : [1, 2, 3, 4], ";
        jsonObjStr += " \"3\" : [1, 2, 3, 4], ";
        jsonObjStr += " \"4\" : [1, 2, 3, 4] ";
        jsonObjStr += " }";*/

        //std::cout << jsonObj << std::endl;
        if(debug==true)
        {
            std::cout << "[INFO]CurlPostRequester post sending: " << jsonObjStr << std::endl;
        }
        //std::cout << jsonObjStr.c_str() << std::endl;
        

        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Accept: application/json");
        headers = curl_slist_append(headers, "Content-Type: application/json");
        headers = curl_slist_append(headers, "charset: utf-8");

        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

        curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonObjStr.c_str());
        //curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonObj);
        curl_easy_setopt(curl, CURLOPT_USERAGENT, "libcrp/0.1");

        // i managed to make it quiet with get reauest with CURLOPT_WRITEFUNCTION
        // but does not work with READFUNCTION callback
        res = curl_easy_perform(curl);
        std::string resStr = std::string(curl_easy_strerror( res ));

        curl_easy_getinfo (curl, CURLINFO_RESPONSE_CODE, &http_code);

        if(debug==true)
        {
            std::cout << "res:" << res << std::endl;
            std::cout << "resstr:" << resStr << std::endl;
            //curl_easy_cleanup(curl);
            std::cout << "http_code:" << http_code << std::endl;
        }

        curl_easy_cleanup(curl);
        curl_global_cleanup();

        if (http_code == 200 && res != CURLE_ABORTED_BY_CALLBACK)
        {
            //Succeeded
            outputMsg = "[INFO]CurlPostRequester success for url: " + url + std::string(", code: ") + std::to_string(http_code);
            if(debug==true){
                std::cout << outputMsg << std::endl;
            }
            return true;
        }
        else if (http_code == 204 && res != CURLE_ABORTED_BY_CALLBACK)
        {
            outputMsg = std::string("[WARNING]CurlPostRequester 204: already uploaded content: ") + url + std::string(", code: ") + std::to_string(http_code) + std::string(", info: ") + resStr;
            if(debug==true){
                std::cout << outputMsg << std::endl;
            }
            return true;
        }
        else
        {
            //Failed
            outputMsg = std::string("[ERROR]CurlPostRequester failed for url: ") + url + std::string(", code: ") + std::to_string(http_code) + std::string(", info: ") + resStr;
            if(debug==true){
                std::cout << outputMsg << std::endl;
            }
            return false;
        }

        outputMsg = std::string("[ERROR]CurlPostRequester bad coding ");
        if(debug==true){
            std::cout << outputMsg << std::endl;
        }
        return false;
    }

    bool post_form(std::string url, std::string data)
    {
        CURL *curl;
        CURLcode res;
        
        struct WriteThis wt;
        
        wt.readptr = data.c_str();
        // wt.sizeleft = strlen(data);
        wt.sizeleft = data.size();
        
        /* In windows, this will init the winsock stuff */
        res = curl_global_init(CURL_GLOBAL_DEFAULT);
        /* Check for errors */
        if(res != CURLE_OK) {
            fprintf(stderr, "curl_global_init() failed: %s\n",
                    curl_easy_strerror(res));
            return 1;
        }
        
        /* get a curl handle */
        curl = curl_easy_init();
        if(curl) {
            /* First set the URL that is about to receive our POST. */
            curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        
            /* Now specify we want to POST data */
            curl_easy_setopt(curl, CURLOPT_POST, 1L);
        
            /* we want to use our own read function */
            curl_easy_setopt(curl, CURLOPT_READFUNCTION, read_callback);
        
            /* pointer to pass to our read function */
            curl_easy_setopt(curl, CURLOPT_READDATA, &wt);
        
            /* get verbose debug output please */
            curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
        
            /*
            If you use POST to an HTTP 1.1 server, you can send data without knowing
            the size before starting the POST if you use chunked encoding. You
            enable this by adding a header like "Transfer-Encoding: chunked" with
            CURLOPT_HTTPHEADER. With HTTP 1.0 or without chunked transfer, you must
            specify the size in the request.
            */
        #ifdef USE_CHUNKED
            {
            struct curl_slist *chunk = NULL;
        
            chunk = curl_slist_append(chunk, "Transfer-Encoding: chunked");
            res = curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
            /* use curl_slist_free_all() after the *perform() call to free this
                list again */
            }
        #else
            /* Set the expected POST size. If you want to POST large amounts of data,
            consider CURLOPT_POSTFIELDSIZE_LARGE */
            curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, (long)wt.sizeleft);
        #endif
        
        #ifdef DISABLE_EXPECT
            /*
            Using POST with HTTP 1.1 implies the use of a "Expect: 100-continue"
            header.  You can disable this header with CURLOPT_HTTPHEADER as usual.
            NOTE: if you want chunked transfer too, you need to combine these two
            since you can only set one list of headers with CURLOPT_HTTPHEADER. */
        
            /* A less good option would be to enforce HTTP 1.0, but that might also
            have other implications. */
            {
            struct curl_slist *chunk = NULL;
        
            chunk = curl_slist_append(chunk, "Expect:");
            res = curl_easy_setopt(curl, CURLOPT_HTTPHEADER, chunk);
            /* use curl_slist_free_all() after the *perform() call to free this
                list again */
            }
        #endif
        
            /* Perform the request, res will get the return code */
            res = curl_easy_perform(curl);
            /* Check for errors */
            if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                    curl_easy_strerror(res));
        
            /* always cleanup */
            curl_easy_cleanup(curl);
        }
        curl_global_cleanup();
        return 0;
    }
    
};


class CurlGetRequester
{
public:
    CURL *curl;
    CURLcode res;
    std::string readBuffer, outputMsg;
    long http_code;
    bool debug = false;
    
	CurlGetRequester()
    {
        curl = curl_easy_init();
    } 
    ~CurlGetRequester()
    {
        curl_easy_cleanup(curl);
    }
    
    bool get(std::string url, bool printContent){
        // return _get(CURLOPT_HTTPGET, url, printContent);
        return _get(url, printContent);
    }
    /*bool post(std::string url, std::string msgToSend, bool printContent){
        if(debug==true) { std::cout << "[DEBUG]Curler::post" << std::endl; }
        readBuffer = msgToSend;
        return _post_or_get(CURLOPT_URL, url, printContent);
    }*/

    // ex: "https://www.ecovision.ovh:81/last_image_filename/polo"
    bool _get(std::string url, bool printContent)
    // bool _get(bool POST, std::string url, bool printContent)
    {
        if(debug==true) { std::cout << "[DEBUG]Curler::_get" << std::endl; }
        http_code = 0;
        // curl = curl_easy_init();
        if(curl) {
            std::string resStr;
            /*if(POST==true){
                if(debug==true) { std::cout << "[DEBUG]Curler::_get post readBuffer: " << readBuffer << std::endl; }
                curl_easy_setopt(curl, CURLOPT_HTTPPOST, 1L);





                const char *data = "============= data to send ============";
                curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

                // size of the POST data 
                curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, 12L);
 
                // pass in a pointer to the data - libcurl will not copy 
                //curl_easy_setopt(curl, CURLOPT_POSTFIELDS, readBuffer.c_str());
                curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
                
                resStr = curl_easy_perform(curl);





            }else{*/
                readBuffer = "";
                curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
            
            curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
            if(debug==true) { std::cout << "[DEBUG]Curler::_get callback" << std::endl; }
            curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
            curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
            if(debug==true) { std::cout << "[DEBUG]Curler::_get perform" << std::endl; }
            res = curl_easy_perform(curl);
            if(debug==true) { std::cout << "[DEBUG]Curler::_get getinfo" << std::endl; }
            curl_easy_getinfo (curl, CURLINFO_RESPONSE_CODE, &http_code);
            resStr = std::string(curl_easy_strerror( res ));
            //}
            if(debug==true)
            {
                std::cout << " =================== " << std::endl;
                std::cout << "res:" << res << std::endl;
                std::cout << "resstr:" << resStr << std::endl;
                std::cout << "readBuffer: " << readBuffer << std::endl;
                //curl_easy_cleanup(curl);
                std::cout << "http_code:" << http_code << std::endl;
            }
                
            // eco i added condition CURLE_OK but just 200 is good enough
            //if (res == CURLE_OK && http_code == 200 && res != CURLE_ABORTED_BY_CALLBACK)
            if (http_code == 200 && res != CURLE_ABORTED_BY_CALLBACK)
            {
                //Succeeded
                outputMsg = "[INFO]curler success for url: " + url + std::string(", code: ") + std::to_string(http_code);
                if(printContent==true){
                    outputMsg += " => " + readBuffer;
                }
                if(debug==true){
                    std::cout << outputMsg << std::endl;
                }
                return true;
            }
            else if (http_code == 204 && res != CURLE_ABORTED_BY_CALLBACK)
            {
                outputMsg = std::string("[WARNING]curler 204: already uploaded content: ") + url + std::string(", code: ") + std::to_string(http_code) + std::string(", info: ") + resStr + std::string(", details: ") + readBuffer;
                if(debug==true){
                    std::cout << outputMsg << std::endl;
                }
                return true;
            }
            else
            {
                //Failed
                outputMsg = std::string("[ERROR]curler failed for url: ") + url + std::string(", code: ") + std::to_string(http_code) + std::string(", info: ") + resStr + std::string(", details: ") + readBuffer;
                if(debug==true){
                    std::cout << outputMsg << std::endl;
                }
                return false;
            }

            if(debug==true){
                std::cout << " =================== " << std::endl;
            }

            
        }
        else
        {
            outputMsg = "[ERROR]curler object badly initialised";
            std::cout << outputMsg << std::endl;
            return false;
        }
        return false;
    }
};

class httpRequestUtils
{
public:
    CurlGetRequester getCurler;
    CurlPostRequester postCurler;

    bool initialised;
    bool printDetails;
    std::string dirForLastCurrentImage;
    std::string uri, camId;
    unsigned int waitIntervalBeforeRetrying, waitTotal;
	
    httpRequestUtils() {initialised=false;dirForLastCurrentImage="";} 
    ~httpRequestUtils() {} 

    void _initialise(std::string _uri, std::string _camId, 
        unsigned int _waitIntervalBeforeRetrying, unsigned int _waitTotal,
        bool _printDetails)
    {
        printDetails = _printDetails;
        uri = _uri;
        camId = _camId;
        waitIntervalBeforeRetrying = _waitIntervalBeforeRetrying;
        waitTotal = _waitTotal;
    }
    bool initialise_for_get(std::string _uri, std::string _camId, 
        std::string tempDirForLastCurrentImage, 
        unsigned int _waitIntervalBeforeRetrying, unsigned int _waitTotal,
        bool _printDetails, std::string _msg)
    {
        _initialise(_uri, _camId, 
            _waitIntervalBeforeRetrying, _waitTotal,
            _printDetails);

        _msg = "";
        dirForLastCurrentImage=tempDirForLastCurrentImage;

        // std::string dirForLastCurrentImage = "./output_simulecovision";
        std::string errStr;
        if(createDirectory(dirForLastCurrentImage, errStr)==0) { 
            _msg = "[ERROR]httpRequestUtils::init: " + errStr;
            if(printDetails==true){
                std::cout << _msg << std::endl;
            }
            return false;
        }
    
        _msg = "[INFO]httpRequestUtils::init: OK";
        if(printDetails==true){
            std::cout << _msg << std::endl;
        }

        initialised=true;
        return true;
    }
    bool initialise_for_post(std::string _uri, std::string _camId, 
        unsigned int _waitIntervalBeforeRetrying, unsigned int _waitTotal,
        bool _printDetails, std::string _msg)
    {
        _initialise(_uri, _camId, 
            _waitIntervalBeforeRetrying, _waitTotal,
            _printDetails);

        _msg = "[INFO]httpRequestUtils::init: OK";
        if(printDetails==true){
            std::cout << _msg << std::endl;
        }

        initialised=true;
        return true;
    }
    
    std::string getExt(std::string filename)
    {
        return filename.substr(filename.find_last_of(".") + 1);
    }

    bool createDirectory(std::string dirName, std::string &_msg)
    {
        _msg = "";
        if(printDetails==true){
            std::cout << "[INFO]httpRequestUtils::createDirectory: " << dirName << std::endl;
        }
        int status = mkdir(dirName.c_str(), 01777); //S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH)!=0) {
        if(status!=0){
            //printf("MKDIR ERROR: %s\n", strerror(errno));
            if(errno==EEXIST){ 
                _msg = ("[INFO]httpRequestUtils::createDirectory: dirout already exists");
                if(printDetails==true){
                    std::cout << _msg << std::endl;
                }
                return true;
            }
            else { 
                // printf("httpRequestUtils::MKDIR ERROR: %s\n", strerror(errno));
                // printf("httpRequestUtils::FAILED to create sub dir '%s' (status %d)\n", dirName.c_str(), status); 
                _msg = "httpRequestUtils::MKDIR ERROR " + std::string(strerror(errno)) + "FAILED to create sub dir " + dirName.c_str() + ", status: " + std::to_string(status);
                if(printDetails==true){
                    std::cout << _msg << std::endl;
                }
                // getchar();
                return false;
            }
        }
        else
        {
            _msg = "[INFO]httpRequestUtils::createDirectory: OK";
            if(printDetails==true){
                std::cout << _msg << std::endl;
            }
            return true;
        }
    }

    bool isValidExt(std::string ext)
    {
        if(ext=="jpg") { return true;}
        if(ext=="jpeg") { return true;}
        if(ext=="JPG") { return true;}
        if(ext=="JPEG") { return true;}
        /*if(ext=="JPG") { return true;}
        if(ext=="png") { return true;}
        if(ext=="ppm") { return true;}
        if(ext=="pgm") { return true;}
        if(ext=="tiff") { return true;}*/
        // what else
        return false;
    }   

    bool getRequestImage_v1(
        std::string &outputSavedImage, 
        //std::ofstream &logfile, 
        std::string &_msg)
    {
        _msg = "";
        outputSavedImage = "";
        if(initialised==false){
            _msg = "[ERROR]httpRequestUtils::getRequestImage: badly initialised> cannot continue";
            if(printDetails==true){
                std::cout << _msg << std::endl;
            }
            return false;
        }

        if(uri.empty()){
            _msg = "[ERROR]httpRequestUtils::getRequestImage: empty uri";
            if(printDetails==true){
                std::cout << _msg << std::endl;
            }
            return false;
        }
        if(camId.empty())
        {
            _msg = "[ERROR]httpRequestUtils::getRequestImage: empty camId";
            if(printDetails==true){
                std::cout << _msg << std::endl;
            }
            return false;
        }

        struct timeval tp;
        gettimeofday(&tp, NULL);
        long int firstMs = tp.tv_sec * 1000 + tp.tv_usec / 1000;
        long int firstSec = firstMs / 1000;

        unsigned int microseconds = waitIntervalBeforeRetrying*1000000;
        while(true)
        {
            //std::string fullUrl1 = uri + "/debug_last_recorded_index/" + camId;
            //std::cout << "[INFO]full url: " << fullUrl1 << '\n';
            //curler.get(fullUrl1);

            // log todo logrorate
            //logfile.open(dirForLastCurrentImage + "/" + camId + ".txt", std::ios_base::app); // append instead of overwrite
            //logfile << getTimeStr() + "[INFO]start\n"; 

            // *** get filename of iage to donwload after ***
            std::string fullUrl1 = uri + "/last_image_filename/" + camId;
            if(printDetails==true){
                std::cout << "[INFO]httpRequestUtils::getRequestImage full url: " << fullUrl1 << '\n';
            }
            //logfile << getTimeStr() + "[INFO]full url:" + fullUrl1 + "\n"; 
            if(getCurler.get(fullUrl1, true)==true)
            {
                std::string filename = getCurler.readBuffer;
                if(printDetails==true){
                    std::cout << filename << std::endl;
                }

                std::string fullUrl3 = uri + "/is_last_image_uploaded/" + camId;
                if(printDetails==true){
                    std::cout << "[INFO]httpRequestUtils::getRequestImage full url: " << fullUrl3 << '\n';
                }
                if(getCurler.get(fullUrl3, true)==true)
                {
                    std::string uploaded = getCurler.readBuffer;
                    if(printDetails==true){
                        std::cout << uploaded << std::endl;
                    }
                    if(uploaded == "False")
                    {
                        //logfile << getTimeStr() + "[INFO]response filename:" + filename + "\n"; 
        
                        // *** get image now ***
                        std::string fullUrl2 = uri + "/last_image_content/" + camId;
                        if(printDetails==true){
                            std::cout << "[INFO]httpRequestUtils::getRequestImage full url: " << fullUrl2 << '\n';
                        }
                        if(getCurler.get(fullUrl2, false)==true)
                        {
                            //if (!output.empty())
                            //{
                            // std::string outputSavedImage = dirForLastCurrentImage + "/" + camId + "_STAMP_" + filename;
                            
                            std::string ext = getExt(filename);
                            std::string outputSavedImageStem = dirForLastCurrentImage + "/" + camId;
                            //logfile << getTimeStr() + "[INFO]outputSavedImage: " + outputSavedImage + "\n"; 
                            std::ofstream outfile{outputSavedImageStem+"."+ext, std::ofstream::binary};
                            //outfile.write(reinterpret_cast<const char*>(response.body.data()),
                                        // static_cast<std::streamsize>(response.body.size()));

                            outfile.write(getCurler.readBuffer.c_str(),
                                        static_cast<std::streamsize>(getCurler.readBuffer.size()));
                            
                            if(isValidExt(ext) == false)
                            {
                                outputSavedImage = outputSavedImageStem + ".jpg";
                                // std::string cmdConvert = "convert " + filename + " " + filename + ".jpg";
                                std::string cmdConvert = "convert " + outputSavedImageStem+"."+ext + " " + outputSavedImageStem + ".jpg";
                                if(printDetails==true){
                                    std::cout << cmdConvert << std::endl;
                                }
                                system(cmdConvert.c_str());
                                //logfile << getTimeStr() + "[ERROR]extension not valid: " + ext + "\n"; 
                                //return EXIT_FAILURE;
                                _msg = "[INFO]httpRequestUtils::getRequestImage converted " + ext + " to jpg => " + outputSavedImage;
                                if(printDetails==true){
                                    std::cout << _msg << std::endl;
                                }
                            }else{
                                outputSavedImage = outputSavedImageStem+"."+ext;
                                _msg = "[INFO]httpRequestUtils::getRequestImage saved => " + outputSavedImage;
                                if(printDetails==true){
                                    std::cout << _msg << std::endl;
                                }
                            }

                            // return to main and std::cout << "[INFO]LAUNCH ECOVISION PROCESS WITH SAVED JPEG IMAGE: " << outputSavedImage << '\n';

                            return true;
                        }
                    }
                    else if(uploaded == "True")
                    {
                        _msg = "[WARNING]httpRequestUtils::getRequestImage image already uploaded, lets wait for next one";
                        if(printDetails==true){
                            std::cout << _msg << std::endl;
                        }
                        //return true;
                    }
                    else
                    {
                        _msg = "[ERROR]httpRequestUtils::getRequestImage uploaded value in response is neither True nor False: " + uploaded;
                        if(printDetails==true){
                            std::cout << _msg << std::endl;
                        }
                        return true;
                    }
                }
            }

            gettimeofday(&tp, NULL);
            long int nowMs = tp.tv_sec * 1000 + tp.tv_usec / 1000;
            long int nowSec = nowMs / 1000;

            if(nowSec - firstSec > waitTotal)
            {
                _msg = "[ERROR]httpRequestUtils::getRequestImage final interval wait reached: stop";
                if(printDetails==true){
                    std::cout << _msg << std::endl;
                }
                return false;
            }

            std::cerr << "[INFO]httpRequestUtils::getRequestImage Sleep for: " << microseconds/1000000 << '\n';
            usleep(microseconds);
        }

        _msg = "[ERROR]httpRequestUtils::getRequestImage loop ended unexpetedly";
        if(printDetails==true){
            std::cout << _msg << std::endl;
        }
        return false;
    }

    bool postRequestJsonMessage(
        std::string &inputMsg, 
        std::string &_msg)
    {

        _msg = "";
        if(initialised==false){
            _msg = "[ERROR]httpRequestUtils::postRequestJsonMessage: badly initialised> cannot continue";
            if(printDetails==true){
                std::cout << _msg << std::endl;
            }
            return false;
        }
        if(uri.empty()){
            _msg = "[ERROR]httpRequestUtils::postRequestJsonMessage: empty uri";
            if(printDetails==true){
                std::cout << _msg << std::endl;
            }
            return false;
        }

        struct timeval tp;
        gettimeofday(&tp, NULL);
        long int firstMs = tp.tv_sec * 1000 + tp.tv_usec / 1000;
        long int firstSec = firstMs / 1000;

        unsigned int microseconds = waitIntervalBeforeRetrying*1000000;
        while(true)
        {
            std::string fullUrl1 = uri + "/result/" + camId;
            if(printDetails==true){
                std::cout << "[INFO]httpRequestUtils::postRequestJsonMessage full url: " << fullUrl1 << '\n';
            }
            //logfile << getTimeStr() + "[INFO]full url:" + fullUrl1 + "\n"; 
            if(postCurler.post_json(fullUrl1, inputMsg)==true)
            {
                if(printDetails==true){
                    std::cout << "[INFO]httpRequestUtils::postRequestJsonMessage posted: " << fullUrl1 << '\n';
                }

                if(postCurler.http_code == 204)
                {
                    _msg = "[INFO]httpRequestUtils::postRequestJsonMessage: code 204 received: " + postCurler.outputMsg;
                    std::cout << postCurler.outputMsg << std::endl; 
                }
                else if(postCurler.http_code == 200)
                {
                    _msg = "[INFO]httpRequestUtils OK";
                    if(printDetails==true){
                        std::cout << _msg << std::endl;
                    }
                    return true;
                }
                else
                {
                    _msg = "[ERROR]wrong http code returned " + std::to_string(getCurler.http_code);
                    if(printDetails==true){
                        std::cout << _msg << std::endl;
                    }
                    return false;
                }
            }
            gettimeofday(&tp, NULL);
            long int nowMs = tp.tv_sec * 1000 + tp.tv_usec / 1000;
            long int nowSec = nowMs / 1000;

            if(nowSec - firstSec > waitTotal)
            {
                _msg = "[ERROR]httpRequestUtils::postRequestJsonMessage final interval wait reached: stop";
                if(printDetails==true){
                    std::cout << _msg << std::endl;
                }
                return false;
            }

            if(printDetails==true){
                std::cerr << "[INFO]httpRequestUtils::postRequestJsonMessage Sleep for: " << microseconds/1000000 << '\n';
            }
            usleep(microseconds);
        }

        _msg = "[ERROR]httpRequestUtils::postRequestJsonMessage loop ended unexpetedly";
        if(printDetails==true){
            std::cout << _msg << std::endl;
        }
        return false;
    }

    bool getRequestImage(
        std::string &outputSavedImage, 
        //std::ofstream &logfile, 
        std::string &_msg)
    {
        _msg = "";
        outputSavedImage = "";
        if(initialised==false){
            _msg = "[ERROR]httpRequestUtils::getRequestImage: badly initialised> cannot continue";
            if(printDetails==true){
                std::cout << _msg << std::endl;
            }
            return false;
        }

        if(uri.empty()){
            _msg = "[ERROR]httpRequestUtils::getRequestImage: empty uri";
            if(printDetails==true){
                std::cout << _msg << std::endl;
            }
            return false;
        }
        if(camId.empty())
        {
            _msg = "[ERROR]httpRequestUtils::getRequestImage: empty camId";
            if(printDetails==true){
                std::cout << _msg << std::endl;
            }
            return false;
        }

        struct timeval tp;
        gettimeofday(&tp, NULL);
        long int firstMs = tp.tv_sec * 1000 + tp.tv_usec / 1000;
        long int firstSec = firstMs / 1000;

        unsigned int microseconds = waitIntervalBeforeRetrying*1000000;
        while(true)
        {
            //std::string fullUrl1 = uri + "/debug_last_recorded_index/" + camId;
            //std::cout << "[INFO]full url: " << fullUrl1 << '\n';
            //curler.get(fullUrl1);

            // log todo logrorate
            //logfile.open(dirForLastCurrentImage + "/" + camId + ".txt", std::ios_base::app); // append instead of overwrite
            //logfile << getTimeStr() + "[INFO]start\n"; 

            // *** get filename of iage to donwload after ***
            std::string fullUrl1 = uri + "/lastimage/" + camId;
            if(printDetails==true){
                std::cout << "[INFO]httpRequestUtils::getRequestImage full url: " << fullUrl1 << '\n';
            }
            //logfile << getTimeStr() + "[INFO]full url:" + fullUrl1 + "\n"; 
            if(getCurler.get(fullUrl1, false)==true)
            {
                if(getCurler.http_code == 204)
                {
                    _msg = "[INFO]httpRequestUtils::getRequestImage: code 204 received: " + getCurler.outputMsg;
                    std::cout << getCurler.outputMsg << std::endl; 
                }
                else if(getCurler.http_code == 200)
                {
                    std::string responseContent = getCurler.readBuffer;
                    if(printDetails==true){
                        //std::cout << responseContent << std::endl;
                    }
                    json j_complete = json::parse(responseContent.c_str());
                    // std::cout << std::setw(4) << j_complete << std::endl;
                    std::string dateTime = j_complete.value("dateTime", "oops");
                    std::string filenameWithStamp = j_complete.value("filenameWithStamp", "oops");
                    std::string hasData = j_complete.value("hasData", "oops");
                    std::string already_uploaded = j_complete.value("uploaded", "oops");
                    std::string contentBytes = j_complete.value("contentBytes", "oops");
                    std::cout << " ... dateTime: " << dateTime << std::endl;
                    std::cout << " ... filenameWithStamp: " << filenameWithStamp << std::endl;
                    std::cout << " ... hasData: " << hasData << std::endl;
                    std::cout << " ... already_uploaded: " << already_uploaded << std::endl;
                    //std::cout << " ... contentBytes: " << contentBytes << std::endl;

                    std::string ext = getExt(filenameWithStamp);
                    std::string outputSavedImageStem = dirForLastCurrentImage + "/" + camId;
                    //logfile << getTimeStr() + "[INFO]outputSavedImage: " + outputSavedImage + "\n";

                    //std::string a = base64_encode(contentBytes, false);
                    std::string b = base64_decode(contentBytes, false);

                    std::ofstream outfile{outputSavedImageStem+"."+ext, std::ofstream::binary};
                    //outfile.write(reinterpret_cast<const char*>(response.body.data()),
                                // static_cast<std::streamsize>(response.body.size()));

                    // outfile.write(getCurler.readBuffer.c_str(),
                    //            static_cast<std::streamsize>(getCurler.readBuffer.size()));
                

                    outfile.write(b.c_str(),
                                static_cast<std::streamsize>(b.size()));

                    if(isValidExt(ext) == false)
                    {
                        outputSavedImage = outputSavedImageStem + ".jpg";
                        // std::string cmdConvert = "convert " + filename + " " + filename + ".jpg";
                        std::string cmdConvert = "convert " + outputSavedImageStem+"."+ext + " " + outputSavedImageStem + ".jpg";
                        if(printDetails==true){
                            std::cout << cmdConvert << std::endl;
                        }
                        system(cmdConvert.c_str());
                        //logfile << getTimeStr() + "[ERROR]extension not valid: " + ext + "\n"; 
                        //return EXIT_FAILURE;
                        //_msg = "[INFO]httpRequestUtils::getRequestImage converted " + ext + " to jpg => " + outputSavedImage;
                        _msg = "[INFO]httpRequestUtils::getRequestImage " + outputSavedImage + " <= " + filenameWithStamp;
                        if(printDetails==true){
                            std::cout << _msg << std::endl;
                        }
                    }else{
                        outputSavedImage = outputSavedImageStem+"."+ext;
                        _msg = "[INFO]httpRequestUtils::getRequestImage saved => " + outputSavedImage;
                        if(printDetails==true){
                            std::cout << _msg << std::endl;
                        }
                    }

                    // return to main and std::cout << "[INFO]LAUNCH ECOVISION PROCESS WITH SAVED JPEG IMAGE: " << outputSavedImage << '\n';

                    _msg = "[INFO]httpRequestUtils OK";
                    if(printDetails==true){
                        std::cout << _msg << std::endl;
                    }
                    return true;
                }
                else
                {
                    _msg = "[ERROR]wrong http code returned " + std::to_string(getCurler.http_code);
                    if(printDetails==true){
                        std::cout << _msg << std::endl;
                    }
                    return false;
                }

            }

            gettimeofday(&tp, NULL);
            long int nowMs = tp.tv_sec * 1000 + tp.tv_usec / 1000;
            long int nowSec = nowMs / 1000;

            if(nowSec - firstSec > waitTotal)
            {
                _msg = "[ERROR]httpRequestUtils::getRequestImage final interval wait reached: stop";
                if(printDetails==true){
                    std::cout << _msg << std::endl;
                }
                return false;
            }

            if(printDetails==true){
                std::cerr << "[INFO]httpRequestUtils::getRequestImage Sleep for: " << microseconds/1000000 << '\n';
            }
            usleep(microseconds);
        }

        _msg = "[ERROR]httpRequestUtils::getRequestImage loop ended unexpetedly";
        if(printDetails==true){
            std::cout << _msg << std::endl;
        }
        return false;
    }
};