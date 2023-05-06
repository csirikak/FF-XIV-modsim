//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

#include <stdio.h>
#include <string.h>
#include <omnetpp.h>

using namespace omnetpp;


class HomeworldPainter : public omnetpp::cSimpleModule {
public:
    HomeworldPainter();
    virtual ~HomeworldPainter();
protected:
    virtual void HomeworldPainter::handleMessage(cMessage *msg);
};

HomeworldPainter::HomeworldPainter()
{

}
HomeworldPainter::~HomeworldPainter()
{

}
Define_Module(HomeworldPainter);

void HomeworldPainter::handleMessage(cMessage *msg)
{
    Job *job = omnetpp::check_and_cast<Job *>(msg);
    double rand = uniform(0, 1.0);
    if(rand < par("rate0"))
    {
        job->setType(0);
    }
    else if(rand > (double)par("rate0")+(double)par("rate1"))
    {
        job->setType(1);
    }
    else if(rand > (double)par("rate0")+(double)par("rate1")+(double)par("rate2"))
    {
        job->setType(2);
    }
    else if(rand > (double)par("rate0")+(double)par("rate1")+(double)par("rate2")+(double)par("rate3"))
    {
        job->setType(3);
    }
    else job->setType(4);
    send(job, "out");
}
/* namespace ffxivproject */
