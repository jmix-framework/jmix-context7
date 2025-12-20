<Path>Add-ons > Charts > Series > Line series > Simple Line series</Path>

LineSeries relates all the data points symbol by broken lines, which is used to show the trend of data changing. It could be used in both rectangular and polar coordinate. Note: with PiecewiseVisualMap component, line chart / area chart can have different colors on different sections.

line-series-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <data readOnly="true">
        <collection id="dateValueDc"
                    class="io.jmix.uisamples.entity.DateValue">
            <fetchPlan extends="_local"/>
            <loader id="dateValueDl" readOnly="true">
                <query>
                    <![CDATA[select e from DateValue e order by e.date]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <charts:chart id="chart" width="100%" height="100%" minHeight="30em">
            <charts:tooltip trigger="AXIS">
                <charts:axisPointer type="CROSS"/>
            </charts:tooltip>

            <charts:dataZoom>
                <charts:sliderDataZoom orientation="HORIZONTAL"
                                       handleIcon="path://M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z"
                                       handleSize="80%"/>
                <charts:sliderDataZoom orientation="VERTICAL" left="5%"
                                       handleIcon="path://M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z"
                                       handleSize="80%"/>
                <charts:insideDataZoom/>
            </charts:dataZoom>

            <charts:xAxes>
                <charts:xAxis type="TIME">
                    <charts:minorSplitLine show="true"/>
                </charts:xAxis>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis>
                    <charts:minorSplitLine show="true"/>
                </charts:yAxis>
            </charts:yAxes>

            <charts:dataSet>
                <charts:source dataContainer="dateValueDc"
                               categoryField="date" valueFields="value"/>
            </charts:dataSet>

            <charts:series>
                <charts:line id="line" name="Value" showSymbol="false"/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




LineSeriesSimpleSample.java

package io.jmix.uisamples.view.flowui.charts.series.line.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("line-series-simple")
@ViewDescriptor("line-series-simple.xml")
public class LineSeriesSimpleSample extends StandardView {
}




DateValue.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDate;
import java.util.UUID;

@JmixEntity
@Table(name = "DATE_VALUE")
@Entity
public class DateValue {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @NotNull
    @Column(name = "DATE_", nullable = false)
    private LocalDate date;

    @NotNull
    @Column(name = "VALUE_", nullable = false)
    private Integer value;

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public LocalDate getDate() {
        return date;
    }

    public Integer getValue() {
        return value;
    }

    public void setValue(Integer value) {
        this.value = value;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    @InstanceName
    @DependsOnProperties({"date", "value"})
    public String getInstanceName() {
        return String.format("%s %s", date, value);
    }
}


