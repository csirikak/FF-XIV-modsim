#include <omnetpp.h>
#include "ffxivsim.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

class MyMessage : public cMessage {
private:
    int myData; // define a payload of type int
public:
    MyMessage(const char *name = nullptr, int kind = 0) : cMessage(name, kind) {
        // initialize the payload to zero
        myData = 0;
    }

    int getPayload() const {
        return myData;
    }

    void setPayload(int data) {
        myData = data;
    }
};
Define_Module(source);

void source::initialize()
{
    arrivalEvent = new cMessage("new player");
    //lambda = par("lambda");
    scheduleAt(simTime() + lambda, arrivalEvent);
}

void source::handleMessage(cMessage *msg)
{
    lambda = exponential(0.01);
    send(msg,"out");
    arrivalEvent = new cMessage("new player");
    scheduleAt(simTime() + lambda, arrivalEvent);
}

void source::finish()
{
}

Define_Module(queue);

void queue::initialize()
{
    queueLengthStats.setName("queueLengthStats");
    queueTimeStats.setName("queueTimeStats");
    sendPlayer = false;
}

void queue::handleMessage(cMessage *msg)
{
    if (msg -> arrivedOn("in"))
    {
        cqueue.insert(msg);
        if (sendPlayer == true) {
            cMessage *nextMsg = (cMessage*)cqueue.pop();
            send(nextMsg, "out");
            sendPlayer = false;
            queueTimeStats.collect(0);
        }
    }
    else if (msg -> arrivedOn("send"))
    {
        u_int len = cqueue.getLength();
        if (len > 0)
        {
            cMessage *nextMsg = (cMessage*)cqueue.pop();
            sendPlayer = false;
            queueTimeStats.collect(simTime() - nextMsg->getCreationTime());
            send(nextMsg, "out");
        }
        else
        {
            sendPlayer = true;
        }
        queueLengthStats.collect(len);
        delete(msg);
    }
}

void queue::finish()
{
    queueLengthStats.recordAs("queueLength");
    queueTimeStats.recordAs("queueTime");
}

Define_Module(classifier);


void classifier::initialize()
{
    for (int i = 0; i<5; i++){
        serverPop[i] = 0;
    }
    maxPlayers = par("maxPlayers");
    cMessage *another = new cMessage("send another player");
    send(another, "send");
}

void classifier::handleMessage(cMessage *msg)
{
    if (msg -> arrivedOn("in"))
    {
        u_int minpop = serverPop[0];
        u_int minIndex = 0;
        for (u_int i = 1; i<5; i++){
            if(serverPop[i] < minpop){
                minpop = serverPop[i];
                minIndex = i;
            }
        }
        send(msg, gate("out", minIndex));
        serverPop[minIndex]++;
        if (serverPop[minIndex] < maxPlayers){
            cMessage *another = new cMessage("send another player");
            send(another, "send");
        }
    }
    else if (msg -> arrivedOn("data"))
    {
        cGate *inputGate = msg->getArrivalGate();
        int gateIndex = inputGate->getIndex();
        MyMessage *updateMsg = check_and_cast<MyMessage *>(msg);
        serverPop[gateIndex] = updateMsg->getPayload();
        if (serverPop[gateIndex] < maxPlayers){
            cMessage *another = new cMessage("send another player");
            send(another, "send");
        }

        delete(msg);
        //delete(updateMsg);
    }
}

void classifier::finish()
{
}

Define_Module(server);

void server::initialize() {
    //mu = par("mu");
    pop = 0;
}
void server::handleMessage(cMessage *msg)
{
    if (msg -> arrivedOn("in")){
        mu = exponential(20);
        scheduleAt(simTime() + mu, new cMessage("departureEvent"));
        delete(msg);
        pop++;
    }
    else {
        pop--;
        MyMessage *update = new MyMessage("population update");
        update->setPayload(pop);
        send(update, "data");
        delete(msg);
    }
}

void server::finish()
{
}

