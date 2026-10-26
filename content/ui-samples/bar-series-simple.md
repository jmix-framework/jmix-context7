<Path>Add-ons > Charts > Series > Bar series > Simple Bar series</Path>

BarSeries shows different data through the height of a bar, which is used in rectangular coordinate with at least one category axis.

bar-series-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:charts="http://jmix.io/schema/charts/ui">
    <data readOnly="true">
        <collection id="countryGrowthDc"
                    class="io.jmix.uisamples.entity.CountryGrowth">
            <fetchPlan extends="_local"/>
            <loader id="countryGrowthDl" readOnly="true">
                <query>
                    <![CDATA[select e from CountryGrowth e]]>
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
                <charts:axisPointer type="SHADOW"/>
            </charts:tooltip>
            <charts:legend top="0"/>

            <charts:xAxes>
                <charts:xAxis/>
            </charts:xAxes>
            <charts:yAxes>
                <charts:yAxis>
                    <charts:axisLabel formatter="{value} %"/>
                </charts:yAxis>
            </charts:yAxes>

            <charts:dataSet>
                <charts:source dataContainer="countryGrowthDc"
                               categoryField="country" valueFields="prevYear currYear"/>
            </charts:dataSet>

            <charts:series>
                <charts:bar name="Previous year"/>
                <charts:bar name="Current year"/>
            </charts:series>
        </charts:chart>
    </layout>
</view>




BarSeriesSimpleSample.java

package io.jmix.uisamples.view.flowui.charts.series.bar.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("bar-series-simple")
@ViewDescriptor("bar-series-simple.xml")
public class BarSeriesSimpleSample extends StandardView {
}




CountryGrowth.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.util.UUID;

@Table(name = "COUNTRY_GROWTH")
@Entity
@JmixEntity
public class CountryGrowth {

    @Id
    @Column(name = "ID")
    @JmixGeneratedValue
    protected UUID id;

    @InstanceName
    @Column(name = "COUNTRY", nullable = false)
    protected String country;

    @Column(name = "FLAG")
    private String flag;

    @Column(name = "PREV_YEAR", nullable = false)
    protected Double prevYear;

    @Column(name = "CURR_YEAR", nullable = false)
    protected Double currYear;

    public CountryGrowth() {
        this.id = UUID.randomUUID();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getFlag() {
        return flag;
    }

    public void setFlag(String flag) {
        this.flag = flag;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public Double getPrevYear() {
        return prevYear;
    }

    public void setPrevYear(Double prevYear) {
        this.prevYear = prevYear;
    }

    public Double getCurrYear() {
        return currYear;
    }

    public void setCurrYear(Double currYear) {
        this.currYear = currYear;
    }
}


