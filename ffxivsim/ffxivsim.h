#ifndef FFXIVSIM_H_
#define FFXIVSIM_H_

using namespace omnetpp;
class source : public cSimpleModule{
    private:
      cMessage *arrivalEvent;
      simtime_t lambda; // Arrival rate
    protected:
      virtual void initialize() override;
      virtual void handleMessage(cMessage *msg) override;
      virtual void finish() override;
};

class queue : public cSimpleModule
{
  private:

    simtime_t mu;  //server rate
    cQueue cqueue;
    bool sendPlayer;
    cHistogram queueLengthStats;
    cHistogram queueTimeStats;

  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
};

class classifier : public cSimpleModule
{
  private:
    cMessage *arrivalEvent;
    cMessage *departureEvent;
    int serverPop[5];     // server population
    int maxPlayers;

  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
};


class server : public cSimpleModule
{
  private:
    int pop;
    simtime_t mu;
  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
};
#endif /* FFXIVSIM_H_ */
