<Path>Cookbook > Compositions > Simple 1-level composition</Path>



This sample demonstrates a one-level composition of `Airport` and `Terminal` entities: the airport contains a collection of terminals. 

Terminals are saved to the database only together with the owning airport, when you click **OK** button in the airport detail view. If you change a terminal and click **OK** in its detail view, but then click **Cancel** in the airport detail view, the terminal changes will not be saved.  

Implementation details: 

- [Airport.java]({currentPath}?tab=Airport.java)
  - `Airport.terminals` attribute is annotated with `@Composition`.

- [airport-detail-view.xml]({currentPath}?tab=airport-detail-view.xml)
  - The fetch plan for loading `Airport` contains the `Airport.terminals` attribute.
  - A nested collection data container is defined for the `Airport.terminals` attribute. 
  - The data grid displaying terminals is connected to this data container.
  - The `create` and `edit` actions of the terminals data grid open the terminal detail view as a dialog (see `<property name="openMode" value="DIALOG"/>`). 


Airport.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.Composition;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.util.List;
import java.util.UUID;

@JmixEntity
@Table(name = "AIRPORT", indexes = {
        @Index(name = "IDX_AIRPORT_CITY", columnList = "CITY_ID")
})
@Entity
public class Airport {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "VERSION", nullable = false)
    @Version
    private Integer version;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    @Column(name = "IATA", length = 3)
    private String iata;

    @JoinColumn(name = "CITY_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private City city;

    @Composition
    @OrderBy("name")
    @OneToMany(mappedBy = "airport")
    private List<Terminal> terminals;

    public Integer getVersion() {
        return version;
    }

    public void setVersion(Integer version) {
        this.version = version;
    }

    public City getCity() {
        return city;
    }

    public void setCity(City city) {
        this.city = city;
    }

    public String getIata() {
        return iata;
    }

    public void setIata(String iata) {
        this.iata = iata;
    }

    public List<Terminal> getTerminals() {
        return terminals;
    }

    public void setTerminals(List<Terminal> terminals) {
        this.terminals = terminals;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}




Terminal.java

package io.jmix.uisamples.entity;

import io.jmix.core.DeletePolicy;
import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.entity.annotation.OnDeleteInverse;
import io.jmix.core.metamodel.annotation.Composition;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.NotNull;

import java.util.List;
import java.util.UUID;

@JmixEntity
@Table(name = "TERMINAL", indexes = {
        @Index(name = "IDX_TERMINAL_AIRPORT", columnList = "AIRPORT_ID")
})
@Entity
public class Terminal {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "VERSION", nullable = false)
    @Version
    private Integer version;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    @OnDeleteInverse(DeletePolicy.CASCADE)
    @JoinColumn(name = "AIRPORT_ID", nullable = false)
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private Airport airport;

    @Column(name = "TERMINAL_TYPE", length = 1)
    private String terminalType;

    @Column(name = "GATE_COUNT")
    private Integer gateCount;

    @Composition
    @OrderBy("name")
    @OneToMany(mappedBy = "terminal")
    private List<MeetingPoint> meetingPoints;

    public TerminalType getTerminalType() {
        return terminalType == null ? null : TerminalType.fromId(terminalType);
    }

    public void setTerminalType(TerminalType terminalType) {
        this.terminalType = terminalType == null ? null : terminalType.getId();
    }

    public Integer getGateCount() {
        return gateCount;
    }

    public void setGateCount(Integer gateCount) {
        this.gateCount = gateCount;
    }

    public List<MeetingPoint> getMeetingPoints() {
        return meetingPoints;
    }

    public void setMeetingPoints(List<MeetingPoint> meetingPoints) {
        this.meetingPoints = meetingPoints;
    }

    public Airport getAirport() {
        return airport;
    }

    public void setAirport(Airport airport) {
        this.airport = airport;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getVersion() {
        return version;
    }

    public void setVersion(Integer version) {
        this.version = version;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}




airport-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://airportDetailView.title"
      focusComponent="form">
    <data>
        <instance id="airportDc"
                  class="io.jmix.uisamples.entity.Airport">
            <fetchPlan extends="_base">
                <property name="city" fetchPlan="_base"/>
                <property name="terminals" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="airportDl"/>
            <collection id="terminalsDc" property="terminals"/>
        </instance>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <actions>
        <action id="saveAction" type="detail_saveClose"/>
        <action id="closeAction" type="detail_close"/>
    </actions>
    <layout>
        <formLayout id="form" dataContainer="airportDc">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="1"/>
                <responsiveStep minWidth="40em" columns="2"/>
            </responsiveSteps>
            <textField id="nameField" property="name"/>
            <textField id="iataField" property="iata"/>
            <entityComboBox id="cityField" property="city">
                <actions>
                    <action id="entityClear" type="entity_clear"/>
                </actions>
                <itemsQuery class="io.jmix.uisamples.entity.City" escapeValueForLike="true"
                            searchStringFormat="(?i)%${inputString}%">
                    <fetchPlan extends="_base"/>
                    <query>
                        <![CDATA[select e from City e where e.name like :searchString escape '\' order by e.name]]>
                    </query>
                </itemsQuery>
            </entityComboBox>
        </formLayout>
        <h4 text="msg://io.jmix.uisamples.entity/Airport.terminals"/>
        <hbox id="buttonsPanel" classNames="buttons-panel">
            <button action="terminalsDataGrid.create"/>
            <button action="terminalsDataGrid.edit"/>
            <button action="terminalsDataGrid.remove"/>
        </hbox>
        <dataGrid id="terminalsDataGrid" dataContainer="terminalsDc" width="100%" minHeight="20em">
            <actions>
                <action id="create" type="list_create">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="terminal-detail-1"/>
                    </properties>
                </action>
                <action id="edit" type="list_edit">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                        <property name="viewId" value="terminal-detail-1"/>
                    </properties>
                </action>
                <action id="remove" type="list_remove"/>
            </actions>
            <columns>
                <column property="name"/>
                <column property="terminalType"/>
                <column property="gateCount"/>
            </columns>
        </dataGrid>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




AirportDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition1;

import io.jmix.flowui.view.EditedEntityContainer;
import io.jmix.flowui.view.StandardDetailView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Airport;

@ViewController(id = "airport-detail-1")
@ViewDescriptor(path = "airport-detail-view.xml")
@EditedEntityContainer("airportDc")
public class AirportDetailView extends StandardDetailView<Airport> {
}




terminal-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://terminalDetailView.title"
      focusComponent="form">
    <data>
        <instance id="terminalDc"
                  class="io.jmix.uisamples.entity.Terminal">
            <fetchPlan extends="_base"/>
            <loader id="terminalDl"/>
        </instance>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <actions>
        <action id="saveAction" type="detail_saveClose"/>
        <action id="closeAction" type="detail_close"/>
    </actions>
    <layout>
        <formLayout id="form" dataContainer="terminalDc">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="1"/>
                <responsiveStep minWidth="40em" columns="2"/>
            </responsiveSteps>
            <textField id="nameField" property="name"/>
            <select id="terminalTypeField" property="terminalType"/>
            <textField id="gateCountField" property="gateCount"/>
        </formLayout>
        <hbox id="detailActions">
            <button id="saveAndCloseButton" action="saveAction"/>
            <button id="closeButton" action="closeAction"/>
        </hbox>
    </layout>
</view>




TerminalDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.composition1;

import io.jmix.flowui.view.EditedEntityContainer;
import io.jmix.flowui.view.StandardDetailView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Terminal;

@ViewController(id = "terminal-detail-1")
@ViewDescriptor(path = "terminal-detail-view.xml")
@EditedEntityContainer("terminalDc")
public class TerminalDetailView extends StandardDetailView<Terminal> {
}


