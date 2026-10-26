<Path>Add-ons > Charts > Series > Scatter series > Large Scatter series</Path>

The chart shows 20,000 points. With `large="true"`, the `scatter` series switches to an optimized rendering mode when the number of points exceeds `largeThreshold` (2000 by default): all points are drawn as one shape instead of separate elements.

The optimization has a price: in this mode, individual points can't have their own styles. A small `symbolSize` and a semi-transparent `itemStyle` make the dense areas of the clusters visible.

Zoom in with the mouse wheel or the sliders. Each axis has its own `insideDataZoom` and `sliderDataZoom`, bound with `xAxisIndexes` or `yAxisIndexes`. `filterMode="EMPTY"` hides the points outside the zoom window instead of removing them from the data, so zooming one axis doesn't change the range of the other.


scatter-series-large.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Large data set" subtext="20,000 points" left="0" top="0"/>

            <charts:xAxes>
                <charts:xAxis type="VALUE" scale="true">
                    <charts:axisLine onZero="false"/>
                </charts:xAxis>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis type="VALUE" scale="true">
                    <charts:axisLine onZero="false"/>
                </charts:yAxis>
            </charts:yAxes>

            <charts:dataZoom>
                <charts:insideDataZoom xAxisIndexes="0" filterMode="EMPTY"/>
                <charts:insideDataZoom yAxisIndexes="0" filterMode="EMPTY"/>
                <charts:sliderDataZoom xAxisIndexes="0" filterMode="EMPTY"/>
                <charts:sliderDataZoom yAxisIndexes="0" orientation="VERTICAL" filterMode="EMPTY"/>
            </charts:dataZoom>

            <charts:series>
                <charts:scatter name="Points" large="true" symbolSize="3">
                    <charts:itemStyle opacity="0.5"/>
                </charts:scatter>
            </charts:series>
        </charts:chart>
    </layout>
</view>




ScatterSeriesLargeSample.java

package io.jmix.uisamples.view.flowui.charts.series.scatter.large;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.chartsflowui.data.item.MapDataItem;
import io.jmix.chartsflowui.kit.component.model.DataSet;
import io.jmix.chartsflowui.kit.data.chart.ListChartItems;
import io.jmix.flowui.view.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;

@ViewController("scatter-series-large")
@ViewDescriptor("scatter-series-large.xml")
public class ScatterSeriesLargeSample extends StandardView {

    private static final int POINT_COUNT = 20_000;

    @ViewComponent
    private Chart chart;

    @Subscribe
    public void onInit(InitEvent event) {
        Random random = new Random();
        double[][] clusterCenters = {{20, 30}, {60, 70}, {75, 25}};

        List<MapDataItem> points = new ArrayList<>(POINT_COUNT);
        for (int i = 0; i < POINT_COUNT; i++) {
            double[] center = clusterCenters[i % clusterCenters.length];
            double x = center[0] + random.nextGaussian() * 10;
            double y = center[1] + random.nextGaussian() * 10;

            points.add(new MapDataItem(Map.of("x", round(x), "y", round(y))));
        }

        chart.setDataSet(
                new DataSet()
                        .withSource(
                                new DataSet.Source<MapDataItem>()
                                        .withDataProvider(new ListChartItems<>(points))
                                        .withValueFields("x", "y")
                        )
        );
    }

    private double round(double value) {
        return Math.round(value * 100) / 100.0;
    }
}


