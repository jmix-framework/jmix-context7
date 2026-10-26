<Path>Add-ons > Charts > Other > Chart with click event</Path>

`ChartClickEvent` is fired when the user clicks a chart element: a pie sector, a bar or a line point. To handle the click, subscribe to the event with `@Subscribe` and the chart id.

`getDetail()` describes the clicked element:

- `seriesName` and `seriesIndex` identify the series;
- `name` and `dataIndex` identify the data item;
- `data` holds the fields of the data item, here `country` and `litres`;
- `percent` is the share of the item in a pie series.

The fields follow the parameters of [ECharts mouse events](https://echarts.apache.org/en/api.html#events.Mouse%20events).

Click a sector to see its value and share. Other mouse events are handled the same way: `ChartDoubleClickEvent`, `ChartMouseDownEvent`, `ChartMouseUpEvent`, `ChartMouseMoveEvent`, `ChartMouseOverEvent` and `ChartMouseOutEvent`.


chart-click-event.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <data readOnly="true">
        <collection id="countryLitresDc"
                    class="io.jmix.uisamples.entity.CountryLitres"
                    fetchPlan="_local">
            <loader id="countryLitresDl" readOnly="true">
                <query>
                    <![CDATA[select e from CountryLitres e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:title text="Liters" subtext="Click a sector to see its value" left="0" top="0"/>
            <charts:legend top="0"/>
            <charts:tooltip trigger="ITEM"/>

            <charts:dataSet>
                <charts:source dataContainer="countryLitresDc"
                               categoryField="country" valueFields="litres"/>
            </charts:dataSet>

            <charts:series>
                <charts:pie name="Liters"/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




ChartClickEventSample.java

package io.jmix.uisamples.view.flowui.charts.other.clickevent;

import io.jmix.chartsflowui.kit.component.event.ChartClickEvent;
import io.jmix.chartsflowui.kit.component.event.dto.ChartClickEventDetail;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("chart-click-event")
@ViewDescriptor("chart-click-event.xml")
public class ChartClickEventSample extends StandardView {

    @Autowired
    private Notifications notifications;

    @Subscribe("chart")
    public void onChartChartClick(final ChartClickEvent event) {
        ChartClickEventDetail detail = event.getDetail();

        String message = "%s: %s liters (%s%%)".formatted(
                detail.getName(), detail.getData().get("litres"), detail.getPercent());
        notifications.show(message);
    }
}




CountryLitres.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

import java.util.UUID;

@JmixEntity
@Table(name = "COUNTRY_LITRES")
@Entity
public class CountryLitres {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @InstanceName
    @NotNull
    @Column(name = "COUNTRY", nullable = false)
    private String country;

    @NotNull
    @Column(name = "LITRES", nullable = false)
    private Double litres;

    public Double getLitres() {
        return litres;
    }

    public void setLitres(Double litres) {
        this.litres = litres;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}


