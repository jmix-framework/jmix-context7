<Path>Fragments > Fragments facets > Settings</Path>

`Settings` facet is designed to persist the state of UI components or custom data in a database in
`FLOWUI_USER_SETTINGS` table.
`UserSettingsItem` JPA entity is used for saving state.

To enable **settings** in a Fragment, it should contain the `SettingsFacet`. The simplest way to add facet is
XML.

Facet with `auto="true"` tries to find all components with defined ID that supports **settings**.
All these components will save and apply their settings.

Supported components:

- `DataGrid`: saves order, sorting and visibility of columns
- `Details`: saves `opened` state
- `SimplePagination`: saves `maxResults`, if `itemsPerPageVisible` attribute is `true`
- `GenericFilter`: saves `opened` state

This sample uses `DataGrid` and `Details` components to demonstrate how settings facet works.
The initial state of the `Details` component is set to `opened`.
You can change this state, then go to another view and return.
The last state will be restored. The same is possible for a `DataGrid` component.


fragment-settings-facet.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <fragment id="fragment"
                  class="io.jmix.uisamples.view.flowui.fragments.facets.settings.SettingsFacetFragment"/>
    </layout>
</view>




FragmentSettingsFacetSample.java

package io.jmix.uisamples.view.flowui.fragments.facets.settings;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("fragment-settings-facet")
@ViewDescriptor("fragment-settings-facet.xml")
public class FragmentSettingsFacetSample extends StandardView {
}




settings-facet-fragment.xml

<fragment xmlns="http://jmix.io/schema/flowui/fragment">
    <data readOnly="true">
        <collection id="customersDc"
                    class="io.jmix.uisamples.entity.Customer"
                    fetchPlan="_local">
            <loader id="customersDl">
                <query>
                    <![CDATA[select e from Customer e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <fragmentSettings auto="true"/>
        <fragmentDataLoadCoordinator auto="true"/>
    </facets>
    <content>
        <vbox padding="false">
            <details id="details" summaryText="DataGrid details" opened="true" width="100%">
                <dataGrid id="customersDataGrid"
                          width="100%"
                          minHeight="20em"
                          columnReorderingAllowed="true"
                          dataContainer="customersDc">
                    <columns>
                        <column property="name"/>
                        <column property="lastName"/>
                        <column property="email"/>
                        <column property="age"/>
                        <column property="active"/>
                        <column property="grade"/>
                    </columns>
                </dataGrid>
            </details>
        </vbox>
    </content>
</fragment>




SettingsFacetFragment.java

package io.jmix.uisamples.view.flowui.fragments.facets.settings;

import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.fragment.Fragment;
import io.jmix.flowui.fragment.FragmentDescriptor;

@FragmentDescriptor("settings-facet-fragment.xml")
public class SettingsFacetFragment extends Fragment<VerticalLayout> {
}


