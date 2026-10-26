<Path>Add-ons > Charts > Series > Gauge series > Ring Gauge series</Path>

A `gauge` series without a pointer can show progress as rings. Each data item becomes a separate ring: `progress` with `overlap="false"` draws the progress bars of the items side by side instead of on top of each other, and `roundCap` rounds their ends.

`startAngle="90"` and `endAngle="-270"` close the scale into a full circle. The scale marks are hidden with `splitLine`, `axisTick` and `axisLabel`, and `pointer` with `show="false"` hides the pointer.

The `title` and `detail` elements of each data item set `offsetCenter`, so the names and the values are stacked in the middle of the rings.


gauge-series-ring.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Project progress" left="0" top="0"/>

            <charts:series>
                <charts:gauge name="Progress" startAngle="90" endAngle="-270">
                    <charts:axisLine>
                        <charts:lineStyle width="40"/>
                    </charts:axisLine>

                    <charts:progress show="true" overlap="false" roundCap="true" clip="false"/>
                    <charts:splitLine show="false"/>
                    <charts:axisTick show="false"/>
                    <charts:axisLabel show="false"/>
                    <charts:pointer show="false"/>

                    <charts:title fontSize="14"/>
                    <charts:detail width="50" height="14" fontSize="14" formatter="{value}%"
                                   color="inherit" borderColor="inherit" borderWidth="1" borderRadius="20"/>

                    <charts:data>
                        <charts:dataItem name="Design" value="80">
                            <charts:title offsetCenter="0% -46%"/>
                            <charts:detail offsetCenter="0% -31%"/>
                        </charts:dataItem>
                        <charts:dataItem name="Development" value="55">
                            <charts:title offsetCenter="0% -8%"/>
                            <charts:detail offsetCenter="0% 7%"/>
                        </charts:dataItem>
                        <charts:dataItem name="Testing" value="30">
                            <charts:title offsetCenter="0% 30%"/>
                            <charts:detail offsetCenter="0% 45%"/>
                        </charts:dataItem>
                    </charts:data>
                </charts:gauge>
            </charts:series>
        </charts:chart>
    </layout>
</view>




GaugeSeriesRingSample.java

package io.jmix.uisamples.view.flowui.charts.series.gauge.ring;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("gauge-series-ring")
@ViewDescriptor("gauge-series-ring.xml")
public class GaugeSeriesRingSample extends StandardView {
}


