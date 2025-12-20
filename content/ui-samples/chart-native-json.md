<Path>Add-ons > Charts > Other > Native JSON</Path>

nativeJson is a universal property that can be used to configure the chart component. An additional JSON options can be set as a string. Most often, this property is suitable for cases where there is on Java API or XML markup for the required options. Note: nativeJson will be merged with existing properties. Also, this property can override options loaded from XML or from component Java API if they overlap. In this sample, the main chart options are set in XML nativeJson tag. It's worth noting that the title property is configured from different places to demonstrate that chart is merging options from JSON. When you click on the chart subtitle you will see the original Apache ECharts example.

chart-native-json.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Native JSON Sample"/>

            <charts:nativeJson>
                <![CDATA[
                {
                "title": {
                    "subtext": 'Click to go to the Apache ECharts source code example'
                },
                "legend": {
                    "show": true,
                    "data": ['Without Round Cap', 'With Round Cap']
                },
                "angleAxis": {
                    "max": 2,
                    "startAngle": 30,
                    "splitLine": {
                        "show": false
                    }
                },
                "radiusAxis": {
                    "type": 'category',
                    "data": ['v', 'w', 'x', 'y', 'z'],
                    "z": 10
                },
                "polar": {},
                "series": [
                    {
                        "type": 'bar',
                        "data": [4, 3, 2, 1, 0],
                        "coordinateSystem": 'polar',
                        "name": 'Without Round Cap',
                        "itemStyle": {
                            "borderColor": 'red',
                            "opacity": 0.8,
                            "borderWidth": 1
                        }
                    },
                    {
                        "type": 'bar',
                        "data": [4, 3, 2, 1, 0],
                        "coordinateSystem": 'polar',
                        "name": 'With Round Cap',
                        "roundCap": true,
                        "itemStyle": {
                            "borderColor": 'green',
                            "opacity": 0.8,
                            "borderWidth": 1
                        }
                    }]
                }
                ]]>
            </charts:nativeJson>
        </charts:chart>
    </layout>
</view>




ChartNativeJsonSample.java

package io.jmix.uisamples.view.flowui.charts.other.nativejson;

import io.jmix.chartsflowui.component.Chart;
import io.jmix.flowui.view.*;

@ViewController("chart-native-json")
@ViewDescriptor("chart-native-json.xml")
public class ChartNativeJsonSample extends StandardView {

    protected static final String SOURCE_ECHARTS_EXAMPLE_LINK =
            "https://echarts.apache.org/examples/en/editor.html?c=polar-roundCap&reset=1&edit=1";

    @ViewComponent
    protected Chart chart;

    @Subscribe
    protected void onInit(InitEvent event) {
        chart.getTitle().setSublink(SOURCE_ECHARTS_EXAMPLE_LINK);
    }
}


