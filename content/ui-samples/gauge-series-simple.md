<Path>Add-ons > Charts > Series > Gauge series > Simple Gauge series</Path>

GaugeSeries use needles to show information as a reading on a dial. Note: Gauge series is the only series that requires an independent description of data in a data. All other series use the DataSet as a data provider.

gauge-series-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart height="100%" width="100%" minHeight="30em">
            <charts:tooltip formatter="{a} &lt;br/&gt;{b} : {c}%"/>

            <charts:series>
                <charts:gauge name="Pressure">
                    <charts:data>
                        <charts:dataItem value="50" name="SCORE"/>
                    </charts:data>
                    <charts:detail formatter="{value}"/>
                </charts:gauge>
            </charts:series>
        </charts:chart>
    </layout>
</view>




GaugeSeriesSimpleSample.java

package io.jmix.uisamples.view.flowui.charts.series.gauge.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("gauge-series-simple")
@ViewDescriptor("gauge-series-simple.xml")
public class GaugeSeriesSimpleSample extends StandardView {
}


