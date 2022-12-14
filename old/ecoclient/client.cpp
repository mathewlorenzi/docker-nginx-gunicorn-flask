//
//  HTTPRequest
//
// g++ ./main.cpp -o ./client
// OK ./client --url http://127.0.0.1:5000/image --method GET --output output.png
// TOTEST ./client --url http://127.0.0.1:5000/lastimage --method GET --output output.png
// KO ./client --url http://127.0.0.1:5000/image --method GET --output output.txt
#include <iostream>
#include <fstream>
#include "HTTPRequest.hpp"
 
//app.py part of thre flask servre
// OK
// /home/ecorvee/Projects/WEBAPP/docker-nginx-gunicorn-flask
/*@app.route("/image", methods=["GET"])
def image():
   filename = os.path.join(get_test_dir(get_root_dir()), "data", "verysmall.jpg")
   with open( filename, mode="rb" ) as f:
       imageContent = f.read()#.decode("iso-8859-1")
       return imageContent*/

// optional
#include <typeinfo>
int main(int argc, const char* argv[])
{
    try
    {
        std::string uri;
        std::string method = "GET";
        std::string arguments;
        std::string output;
        auto protocol = http::InternetProtocol::V4;
        for (int i = 1; i < argc; ++i)
        {
            const auto arg = std::string{argv[i]};
            if (arg == "--help")
            {
                std::cout << "example --url <url> [--protocol <protocol>] [--method <method>] [--arguments <arguments>] [--output <output>]\n";
                return EXIT_SUCCESS;
            }
            else if (arg == "--url")
            {
                if (++i < argc) uri = argv[i];
                else throw std::runtime_error("Missing argument for --url");
            }
            else if (arg == "--protocol")
            {
                if (++i < argc)
                {
                    if (std::string{argv[i]} == "ipv4")
                        protocol = http::InternetProtocol::V4;
                    else if (std::string{argv[i]} == "ipv6")
                        protocol = http::InternetProtocol::V6;
                    else
                        throw std::runtime_error{"Invalid protocol"};
                }
                else throw std::runtime_error{"Missing argument for --protocol"};
            }
            else if (arg == "--method")
            {
                if (++i < argc) method = argv[i];
                else throw std::runtime_error{"Missing argument for --method"};
            }
            else if (arg == "--arguments")
            {
                if (++i < argc) arguments = argv[i];
                else throw std::runtime_error{"Missing argument for --arguments"};
            }
            else if (arg == "--output")
            {
                if (++i < argc) output = argv[i];
                else throw std::runtime_error{"Missing argument for --output"};
            }
            else
                throw std::runtime_error{"Invalid flag: " + arg};
        }
        http::Request request{uri, protocol};
        const auto response = request.send(method, arguments, {
            {"Content-Type", "application/x-www-form-urlencoded"},
            {"User-Agent", "runscope/0.1"},
            {"Accept", "*/*"}
        }, std::chrono::seconds(2));
        std::cout << "response.status.reason: " << response.status.reason << '\n'; // e.g. OK
        if (response.status.code == http::Status::Ok)
        {
            if (!output.empty())
            {
                std::ofstream outfile{output, std::ofstream::binary};
                outfile.write(reinterpret_cast<const char*>(response.body.data()),
                              static_cast<std::streamsize>(response.body.size()));
            }
            else
            {
                std::cout << "output not specified. " << std::string{response.body.begin(), response.body.end()} << '\n';
            }
            //const char* dataPt = reinterpret_cast<const char*>(response.body.data());
            //std::string dataString(dataPt);
            
            //std::cout << "dataString: " << dataString << std::endl;
            
            //FILE* pFile;
            //pFile = fopen("output.png", "wb");
            /*for (unsigned long long j = 0; j < 1024; ++j){
                //Some calculations to fill a[]
                fwrite(dataPt, 1, size*sizeof(unsigned long long), pFile);
            }*/
            /*size_t bytes = dataString.length();
            std::cout << "nb bytes: " << bytes << std::endl;
            fwrite(&dataPt[0], 1, bytes, pFile);
            fclose(pFile);
            return 0;*/
                
            //char* dataPt = reinterpret_cast<char*>(response.body.data());
            //std::cout << "dataPt:" << dataPt << '\n';
            /*char* p = NULL;
            int i=0;
            while(*p != '\0'){
                *p = dataPt[i];
                //std::cout << p;
                i++;
            }
            p = NULL;*/
            
            /*char* p = &dataPt[0];
            while(*p != '\0') {
                //process the current char
                ++p;  //you can increment pointers without assigning an address to them
            }*/
        }
    }
    catch (const http::RequestError& e)
    {
        std::cerr << "Request error: " << e.what() << '\n';
        return EXIT_FAILURE;
    }
    catch (const http::ResponseError& e)
    {
        std::cerr << "Response error: " << e.what() << '\n';
        return EXIT_FAILURE;
    }
    catch (const std::exception& e)
    {
        std::cerr << "Error: " << e.what() << '\n';
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
 