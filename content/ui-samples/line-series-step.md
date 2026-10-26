<Path>Add-ons > Charts > Series > Line series > Step Line series</Path>

A step line connects the points with horizontal and vertical segments instead of slopes. It suits values that change in jumps and stay the same between the changes, such as prices or rates.

The `step` attribute of the `line` series sets where the vertical segment is drawn:

- `START` — at the start point;
- `MIDDLE` — halfway between the points;
- `END` — at the end point.


line-series-step.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:legend top="0"/>
            <charts:tooltip trigger="AXIS"/>

            <charts:xAxes>
                <charts:xAxis type="CATEGORY"/>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis/>
            </charts:yAxes>

            <charts:series>
                <charts:line name="Step start" step="START"/>
                <charts:line name="Step middle" step="MIDDLE"/>
                <charts:line name="Step end" step="END"/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




LineSeriesStepSample.java

package io.jmix.uisamples.view.flowui.charts.series.line.step;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.view.*;

import java.util.Map;

@ViewController("line-series-step")
@ViewDescriptor("line-series-step.xml")
public class LineSeriesStepSample extends StandardView {

    @ViewComponent
    private Chart chart;

    @Subscribe
    public void onInit(InitEvent event) {
        ListChartItems<MapDataItem> items = new ListChartItems<>(
                createItem("Mon", 120, 220, 450),
                createItem("Tue", 132, 282, 432),
                createItem("Wed", 101, 201, 401),
                createItem("Thu", 134, 234, 454),
                createItem("Fri", 90, 290, 590),
                createItem("Sat", 230, 430, 530),
                createItem("Sun", 210, 410, 510)
        );

        chart.setDataSet(
                new DataSet()
                        .withSource(
                                new DataSet.Source<MapDataItem>()
                                        .withDataProvider(items)
                                        .withCategoryField("day")
                                        .withValueFields("start", "middle", "end")
                        )
        );
    }

    private MapDataItem createItem(String day, int start, int middle, int end) {
        return new MapDataItem(Map.of("day", day,
                "start", start,
                "middle", middle,
                "end", end));
    }
}


