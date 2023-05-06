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

package ffxivproject.simulations;

import org.omnetpp.queueing.Classifier;
import org.omnetpp.queueing.PassiveQueue;
import org.omnetpp.queueing.Queue;
import org.omnetpp.queueing.Server;
import org.omnetpp.queueing.Source;
import ffxivproject.HomeworldPainter;

//
// Sample network, consisting of a source and a sink.
//
network SourceSink
{
    submodules:
        Crystal: Queue {
            @display("p=331,82;i=,lightblue");
        }
        Balmung: Queue {
            @display("p=331,160;i=,aquamarine");
        }
        Primal: Queue {
            @display("p=331,231;i=,orchid");
        }
        Omega: Queue {
            @display("p=331,308;i=,coral");
        }
        Garuda: Queue {
            @display("p=331,382;i=,lightgreen");
        }
        sink: org.omnetpp.queueing.Sink {
            @display("p=434,231");
        }
        classifier: Classifier {
            @display("p=235,231");
        }
        source: Source {
            @display("p=50,141");
        }
        DCQueue: Queue {
            @display("p=50,231");
        }
        homeworldPainter: HomeworldPainter {
            @display("p=136,231");
        }
    connections:
        Crystal.out --> sink.in++;
        Balmung.out --> sink.in++;
        Primal.out --> sink.in++;
        Omega.out --> sink.in++;
        Garuda.out --> sink.in++;
        classifier.out++ --> Crystal.in++;
        classifier.out++ --> Balmung.in++;
        classifier.out++ --> Primal.in++;
        classifier.out++ --> Omega.in++;
        classifier.out++ --> Garuda.in++;
        source.out --> DCQueue.in++;
        DCQueue.out --> homeworldPainter.in;
        homeworldPainter.out --> classifier.in++;
}

