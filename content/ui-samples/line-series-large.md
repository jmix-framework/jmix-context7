<Path>Add-ons > Charts > Series > Line series > Large Line series</Path>

The chart shows 20,000 points, many more than the pixels across it. `sampling` makes the `line` series draw only some of the points while keeping the shape of the line:

- `LARGEST_TRIANGLE_THREE_BUCKET` — the LTTB algorithm keeps the points that define the shape best, including peaks;
- `AVERAGE`, `MAX`, `MIN` and `SUM` — replace each group of points with one aggregated value.

`showSymbol="false"` hides the point markers, which are not visible at this density anyway. Zoom in with the mouse wheel or the slider: the fewer points fall into the visible range, the more of them the chart draws.


line-series-large.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Large data set" subtext="20,000 points" left="0" top="0"/>
            <charts:tooltip trigger="AXIS"/>

            <charts:xAxes>
                <charts:xAxis type="TIME"/>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis/>
            </charts:yAxes>

            <charts:dataZoom>
                <charts:insideDataZoom/>
                <charts:sliderDataZoom/>
            </charts:dataZoom>

            <charts:series>
                <charts:line name="Value" showSymbol="false" sampling="LARGEST_TRIANGLE_THREE_BUCKET">
                    <charts:areaStyle/>
                </charts:line>
            </charts:series>
        </charts:chart>
    </layout>
</view>




LineSeriesLargeSample.java

package io.jmix.uisamples.view.flowui.charts.series.line.large;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.view.*;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;

@ViewController("line-series-large")
@ViewDescriptor("line-series-large.xml")
public class LineSeriesLargeSample extends StandardView {

    private static final int POINT_COUNT = 20_000;

    @ViewComponent
    private Chart chart;

    @Subscribe
    public void onInit(InitEvent event) {
        Random random = new Random();
        LocalDate startDate = LocalDate.of(1970, 1, 1);
        double value = 1000;

        List<MapDataItem> points = new ArrayList<>(POINT_COUNT);
        for (int i = 0; i < POINT_COUNT; i++) {
            value = Math.max(0, value + random.nextDouble(-20, 21));
            points.add(new MapDataItem(Map.of("date", startDate.plusDays(i), "value", Math.round(value))));
        }

        chart.setDataSet(
                new DataSet()
                        .withSource(
                                new DataSet.Source<MapDataItem>()
                                        .withDataProvider(new ListChartItems<>(points))
                                        .withCategoryField("date")
                                        .withValueField("value")
                        )
        );
    }
}


