/*
        AtlasSocket.cpp
        ----------------
        begin           : 1999.11.29
        copyright       : (C) 1999 by John Barrett (ZW)
        email           : jbarrett@box100.com
*/

#include <cassert>
#include <cstdlib>

#include "../Object/Debug.h"
#include "TCPSocket.h"

#if defined(_WIN32) || defined(__WINDOWS__)
int ATCPSocket::didWSAInit = 0;
#else
#include <fcntl.h>
#endif

const u_long ADDRESS_ERROR = 0xFFFFFFFF;

ATCPSocket::ATCPSocket()
{

#if defined(_WIN32) || defined(__WINDOWS__)
	if (!didWSAInit) {
		WSAStartup(0x0101, &wsadata);
		didWSAInit = 1;
		DebugMsg1(4, "ATCPSocket :: Did WSAStartup\n\n");
	}
#endif

	sock = socket(AF_INET, SOCK_STREAM, 0);
	DebugMsg1(4, "ATCPSocket :: Created Socket=%li", (long)sock);
}

ATCPSocket::~ATCPSocket()
{
#ifndef _WIN32
	::close(sock);
	sock = (SOCKET)-1;
#endif
}

ATCPSocket::ATCPSocket(SOCKET asock): ASocket(asock)
{
}

int	ATCPSocket::connect(const string& addr, int port)
{
    struct hostent      *host;
    u_long              hostaddr;
    struct sockaddr_in  sin;
    int                 res;

    host = gethostbyname(addr.c_str());
    if (host == NULL)
	{
        //convert string to IP address
        hostaddr = inet_addr(addr.c_str());
        DebugMsg1(4, "ATCPSocket :: Converted IP Address = %li \n", hostaddr);
        if ( hostaddr == ADDRESS_ERROR )
            return -1;
    } else {
        // name lookup worked, get address
        DebugMsg1(4, "ATCPSocket :: Reading host entry\n","");
        hostaddr = *((u_long *)host->h_addr);
    }

    DebugMsg3(4, "ATCPSocket :: Opening connection to %li:%i on socket = %i\n", hostaddr,port,sock);

    memset(&sin, 0, sizeof(sin)); // make sure everything zero
    sin.sin_family = AF_INET;
    sin.sin_port = htons(port);
    sin.sin_addr.s_addr = hostaddr;

    res=::connect(sock, (struct sockaddr*)&sin, sizeof(sin));

    return res;
}

int	ATCPSocket::listen(const string& addr, int port, int backlog)
{
	u_long              myaddr;
	struct sockaddr_in  sin;
	int                 res;

	myaddr = inet_addr(addr.c_str());
	if (myaddr == ADDRESS_ERROR )
	    return -1;

	memset(&sin, 0, sizeof(sin)); // make sure everything zero
	sin.sin_family = AF_INET;
	sin.sin_port = htons(port);
	sin.sin_addr.s_addr = myaddr;

	res = bind(sock, (struct sockaddr*)&sin, sizeof(sin));
	if (res == -1)
	    return -1;

	return ::listen(sock, backlog);
}

ASocket*	ATCPSocket::accept()
{
	int			newsock;
	struct sockaddr_in	sin;
	sinlen_t			sinlen;

	sinlen = sizeof(sin);
	newsock = ::accept(sock, (struct sockaddr*)&sin, &sinlen);
	return new ATCPSocket(newsock);
}

int	ATCPSocket::send(const string& data)
{
	DebugMsg2(4, "Sending Data on Socket=%li Data=%s", (long)sock, data.c_str());
	return ::send(sock, data.c_str(), data.length(), 0);
}

int		ATCPSocket::recv(string& data)
{
	char	buf[2048];

	int res = ::recv(sock,buf,2047,0);
    if(res<0)
        res=0;

	data.erase();
	data.assign(buf,res);
	return res;
}

