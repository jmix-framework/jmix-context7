<Path>Add-ons > Charts > Series > Gauge series > Colorized Gauge series</Path>

Different areas of the series can be colored using the colorPalette property for the Axis Line.

gauge-series-colorized.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <facets>
        <timer id="timer"
               delay="2000"
               autostart="true"
               repeating="true"/>
    </facets>
    <layout>
        <charts:chart id="chart" height="100%" width="100%" minHeight="30em">

            <charts:series>
                <charts:gauge id="gaugeSeries">
                    <charts:axisLine>
                        <charts:lineStyle width="30">
                            <charts:colorPalette>
                                <charts:colorItem range="0.2" color="#67e0e3"/>
                                <charts:colorItem range="0.8" color="#37a2da"/>
                                <charts:colorItem range="1" color="#ff0000"/>
                            </charts:colorPalette>
                        </charts:lineStyle>
                    </charts:axisLine>

                    <charts:pointer>
                        <charts:itemStyle color="auto"/>
                    </charts:pointer>

                    <charts:axisTick distance="-30" length="8">
                        <charts:lineStyle color="WHITE" width="2"/>
                    </charts:axisTick>

                    <charts:splitLine distance="-30" length="30">
                        <charts:lineStyle color="WHITE" width="4"/>
                    </charts:splitLine>

                    <charts:axisLabel color="inherit" distance="40" fontSize="20"/>

                    <charts:detail valueAnimation="true" formatter="{value} km/h" color="inherit"/>

                    <charts:data>
                        <charts:dataItem value="70"/>
                    </charts:data>
                </charts:gauge>
            </charts:series>
        </charts:chart>
    </layout>
</view>




GaugeSeriesColorizedSample.java

package io.jmix.uisamples.view.flowui.charts.series.gauge.colorized;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.kit.component.model.series.GaugeSeries;
import io.jmix.flowui.facet.Timer;
import io.jmix.flowui.view.*;

import java.util.Random;

@ViewController("gauge-series-colorized")
@ViewDescriptor("gauge-series-colorized.xml")
public class GaugeSeriesColorizedSample extends StandardView {

    @ViewComponent
    protected Chart chart;

    protected Random random = new Random();

    @Subscribe("timer")
    protected void onTimerTick(Timer.TimerActionEvent event) {
        GaugeSeries gaugeSeries = chart.getSeries("gaugeSeries");

        gaugeSeries.setData(
                new GaugeSeries.DataItem()
                        .withValue((double) random.nextInt(0, 100))
        );
    }
}


