simple source
{
    parameters:
        @display("i=block/source");
        int samples = default(1000000);
    gates:
        output out;
}

simple queue
{
    parameters:
        @display("i=block/queue");
    gates:
        input in;
        input send;
        output out;
}

simple classifier
{
    parameters:
        @display("i=block/classifier_l");
        int maxPlayers = default(60);
    gates:
        input in;
        output send;
        output out[5];
        input data[5];
}

simple server
{
    parameters:
        @display("i=block/server");
    gates:
        input in;
        output data;
}

network Ffxivsim
{
    @display("bgb=986,526");
    submodules:
        source: source {
            @display("p=27.939999,132.08");
        }
        queue: queue {
            @display("p=176.10666,132.08");
        }
        classifier: classifier {
            @display("p=256.10666,132.08");
        }
        Crystal: server {
            @display("p=333.58667,50.08");
        }
        Balmung: server {
            @display("p=333.58667,152.08");
        }
        Primal: server {
            @display("p=333.58667,252.08");
        }
        Omega: server {
            @display("p=333.58667,352.08");
        }
        Garuda: server {
            @display("p=333.58667,452.08");
        }
    connections:
        source.out --> queue.in;
        queue.out --> classifier.in;
        classifier.send --> queue.send;
        classifier.out[0] --> Crystal.in;
        classifier.out[1] --> Balmung.in;
        classifier.out[2] --> Primal.in;
        classifier.out[3] --> Omega.in;
        classifier.out[4] --> Garuda.in;
        Crystal.data --> classifier.data[0];
        Balmung.data --> classifier.data[1];
        Primal.data --> classifier.data[2];
        Omega.data --> classifier.data[3];
        Garuda.data --> classifier.data[4];
}

