<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:local="local" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" exclude-result-prefixes="#all" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:link="http://www.xbrl.org/2003/linkbase" xmlns:utr="http://www.xbrl.org/2009/utr" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:conf="http://edgar/2009/conformance" xmlns="http://www.xbrl.org/2003/instance">
  <!-- the purpose of this stylesheet is to transform a previously generated edgar-20101231.xsd into testcases. 2010 is the parameter called "year" in both stylesheets. -->
  <!-- /bin/bash
  transform -xsl:utr2schema.xsl -s:../../lib/utr.xml
  transform -xsl:schema2testcases.xsl -s:tmp/edgar-20101231.xsd 
  dirclean.sh .
  -->
   <xsl:import href="../../../xsl/fttd.xsl"/>
  <xsl:output method="xml" encoding="UTF-8" indent="yes" exclude-result-prefixes="#all" xmlns=""/>
  <xsl:param name="schema">edgar</xsl:param>
  <xsl:param name="year">2010</xsl:param>
  <xsl:param name="fyear">2008</xsl:param>
  <xsl:param name="testcase">605-35-numeric-units-testcase</xsl:param>
  <xsl:param name="date">2017-07-12</xsl:param>
  <xsl:param name="version">50</xsl:param>
  <xsl:param name="page">6-17</xsl:param>
  <xsl:variable name="sp" select="' '"/>
  <xsl:variable name="nl" select="'&#xA;'"/>
  <xsl:variable name="us" select="'_'"/>
  <xsl:variable name="sl" select="'/'"/>
  <xsl:variable name="co" select="':'"/>
  <xsl:variable name="nsXbrli">http://www.xbrl.org/2003/instance</xsl:variable>
  <xsl:variable name="nsLink">http://www.xbrl.org/2003/linkbase</xsl:variable>
  <xsl:variable name="nsXlink">http://www.w3.org/1999/xlink</xsl:variable>
  <xsl:variable name="nsConformance">http://edgar/2009/conformance</xsl:variable>
  <xsl:variable name="prefix">edgar</xsl:variable>
  <xsl:variable name="nsTarget">
    <xsl:value-of select="concat('http://edgar/',$year,'1231')"/>
  </xsl:variable>
  <xsl:variable name="nsIso">http://www.xbrl.org/2003/iso4217</xsl:variable>
  <xsl:variable name="nsDei">http://xbrl.sec.gov/dei/2018-01-31</xsl:variable>
  <xsl:variable name="good" select="concat('e60535','000','gd','-',$year,'1231')"/>
  <xsl:template match="xs:schema">
    <xsl:result-document href="{$schema}-{$year}1231.xsd" method="xml" encoding="UTF-8" indent="yes" exclude-result-prefixes="#all">
      <xsl:apply-templates select="." mode="clean"/>
    </xsl:result-document>
    <xsl:result-document href="{$schema}-{$year}1231_lab.xml" method="xml" encoding="UTF-8" indent="yes" exclude-result-prefixes="#all">
      <xsl:copy-of select="doc(concat('tmp/',$schema,'-',$year,'1231_lab.xml'))"/>
    </xsl:result-document>
    <xsl:result-document href="{$schema}-{$year}1231_pre.xml" method="xml" encoding="UTF-8" indent="yes" exclude-result-prefixes="#all">
      <xsl:copy-of select="doc(concat('tmp/',$schema,'-',$year,'1231_pre.xml'))"/>
    </xsl:result-document>

    <xsl:result-document href="{$testcase}.xml" method="xml" encoding="UTF-8" indent="yes" exclude-result-prefixes="#all">
      <xsl:processing-instruction name="xml-stylesheet">type="text/xsl" href="../../../lib/test.xsl"</xsl:processing-instruction>

      <conf:testcase xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:conf="http://edgar/2009/conformance" xsi:schemaLocation="http://edgar/2009/conformance ../../../lib/test.xsd">
        <conf:creator>
          <conf:name>SEC Office of Structured Disclosure</conf:name>
          <conf:email>StructuredData@sec.gov</conf:email>
        </conf:creator>
        <conf:number>605-35</conf:number>
        <conf:name>EDGAR Filer Manual v<xsl:value-of select="$version"/> 6.5.35 page <xsl:value-of select="$page"/></conf:name>
        <conf:description>
          <h2>If element "UTR" in a standard namespace is declared in the DTS of an instance, then the value of each 'unitRef' attribute on each fact of a type in that registry must refer to a unit declaration consistent with the data type of that fact, where consistency is defined by that registry.</h2>
          <p>XBRL 2.1 already enforces the requirement that a fact of type xbrli:monetaryItemType must have a unitRef whose xbrli:measure is an ISO standard currency. A standard numeric data type registry is similar but broader: it has a schema with numeric type declarations, and each numeric data type is associated with consistent unit declaration measures, numerators and denominators.</p>
          <p>A portion of a registry is shown below; additional information is at <a href="http://www.sec.gov/info/edgar/edgartaxonomies.shtml">http://www.sec.gov/edgar/info/edgartaxonomies.shtml</a>.</p>
          <table style="font-family: Arial; font-size: smaller; cell-spacing:0pt; border:solid black 1pt">
            <tr>
              <th>Type name-space</th>
              <th>Type element name</th>
              <th>Unit measure name-space</th>
              <th>Unit measure element names</th>
              <th>Meaning</th>
              <th>Unit numerator name-space</th>
              <th>Unit numerator element name</th>
              <th>Unit denominator namespace</th>
              <th>Unit denominator element name</th>
            </tr>
            <tr valign="top">
              <td>(any)</td>
              <td>percentItemType</td>
              <td>xbrli</td>
              <td>pure</td>
              <td>&#160;</td>
              <td>n/a</td>
              <td>disallowed</td>
              <td>n/a</td>
              <td>disallowed</td>
            </tr>
            <tr valign="top">
              <td>(any)</td>
              <td>perShareItemType</td>
              <td>n/a</td>
              <td>disallowed</td>
              <td>&#160;</td>
              <td>iso4217</td>
              <td>
                <span style="white-space: nowrap;">3-letter ISO</span> 4217 codes</td>
              <td>xbrli</td>
              <td>shares</td>
            </tr>
            <tr valign="top">
              <td rowspan="7" valign="top">(any)</td>
              <td rowspan="7" valign="top">areaItemType</td>
              <td rowspan="7" valign="top">(any)</td>
              <td>sqft</td>
              <td>Square Foot</td>
              <td rowspan="7" valign="top">n/a</td>
              <td rowspan="7" valign="top">disallowed</td>
              <td rowspan="7" valign="top">n/a</td>
              <td rowspan="7" valign="top">disallowed</td>
            </tr>
            <tr valign="top">
              <td>sqyd</td>
              <td>Square Yard</td>
            </tr>
            <tr valign="top">
              <td>sqmi</td>
              <td>Square Mile</td>
            </tr>
            <tr valign="top">
              <td>A</td>
              <td>Acre</td>
            </tr>
            <tr valign="top">
              <td>sqm</td>
              <td style="white-space: nowrap">Square Meter</td>
            </tr>
            <tr valign="top">
              <td>sqkm</td>
              <td>Square Km</td>
            </tr>
            <tr valign="top">
              <td>sqemi</td>
              <td>Square English Mile</td>
            </tr>
            <tr valign="top">
              <td rowspan="10" valign="top">(any)</td>
              <td rowspan="10" valign="top">volumeItemType</td>
              <td rowspan="10" valign="top">(any)</td>
              <td>l</td>
              <td>Liter</td>
              <td rowspan="10" valign="top">n/a</td>
              <td rowspan="10" valign="top">disallowed</td>
              <td rowspan="10" valign="top">n/a</td>
              <td rowspan="10" valign="top">disallowed</td>
            </tr>
            <tr valign="top">
              <td>m3</td>
              <td>Cubic Meter</td>
            </tr>
            <tr valign="top">
              <td>ft3</td>
              <td>Cubic Foot</td>
            </tr>
            <tr valign="top">
              <td>gal</td>
              <td>Gallon</td>
            </tr>
            <tr valign="top">
              <td>cf</td>
              <td>Cubic Feet of Natural Gas at 14.73psi and 60 degrees F</td>
            </tr>
            <tr valign="top">
              <td>Mcf</td>
              <td>Thousands of Cubic Feet of Natural Gas at 14.73psi and 60 degrees F</td>
            </tr>
            <tr valign="top">
              <td>MMcf</td>
              <td>Millions of Cubic Feet of Natural Gas at 14.73psi and 60 degrees F</td>
            </tr>
            <tr valign="top">
              <td>bbl</td>
              <td>Barrels of Oil at 60 degrees F</td>
            </tr>
            <tr valign="top">
              <td>MBbls</td>
              <td>Thousands of Barrels of Oil at 60 degrees F</td>
            </tr>
            <tr valign="top">
              <td>MMbbls</td>
              <td>Millions of Barrels of Oil at 60 degrees F</td>
            </tr>
          </table>
          <p>In this table, for example, facts whose type is based on areaItemType must have a unit whose measure is one of sqft, sqyd, sqmi, etc. The notation "(any)" means that the element namespace is ignored for the purposes of checking for consistency.</p>
        </conf:description>
        <conf:variation id="_000gd">
          <conf:name>6.5.35, Instance with all compatible combinations of numeric type and unit on directly typed concepts, GOOD.</conf:name>
          <conf:description>Instance with all compatible combinations of numeric type and unit on directly typed concepts, GOOD.</conf:description>
          <conf:data>
            <conf:instance readMeFirst="true"><xsl:value-of select="$good"/>.xml</conf:instance>
            <conf:linkbase><xsl:value-of select="concat($schema,'-',$year,'1231')"/>_pre.xml</conf:linkbase>
            <conf:linkbase><xsl:value-of select="concat($schema,'-',$year,'1231')"/>_lab.xml</conf:linkbase>            
            <conf:linkbase><xsl:value-of select="concat($schema,'-',$year,'1231')"/>_def.xml</conf:linkbase>
            <conf:schema><xsl:value-of select="concat($schema,'-',$year,'1231')"/>.xsd</conf:schema>
          </conf:data>
          <conf:result/>
        </conf:variation>
        <xsl:for-each select="xs:element/xs:annotation/xs:documentation[@source='nogood']/*">
          <xsl:variable name="element" select="ancestor::xs:element/@name"/>
          <xsl:variable name="unit" select="."/>
          <xsl:variable name="seq" select="format-number(position()+1,'000')"/>
          <xsl:variable name="id" select="concat($us,$seq,'ng')"/>
          <xsl:variable name="base" select="concat('e60535',$seq,'ng','-',$year,'1231')"/>
          <xsl:variable name="pretty" select="concat($element,' fact with '
              ,(if (contains(@id,'__x')) then
                concat('locally defined unit ',substring-after(@id,'__x'))
                else
                concat('unit ',substring-after(@id,'__'))),
                ', NOGOOD')"/>
          <conf:variation id="{$id}">
            <conf:name>
              <xsl:text>6.5.35, </xsl:text>
              <xsl:value-of select="$pretty"/>
            </conf:name>
            <conf:description>
              <xsl:value-of select="$pretty"/>
            </conf:description>
            <conf:data>              
              <conf:parameter xmlns="" name="ELOparams" 
                value="{local:json(('periodOfReport','12-31-2008',
                'emergingGrowthCompanyFlag', 'false',
                'submissionType', '8-K'))}"/>
              <conf:instance readMeFirst="true"><xsl:value-of select="$base"/>.xml</conf:instance>
              <conf:linkbase><xsl:value-of select="concat($schema,'-',$year,'1231')"/>_pre.xml</conf:linkbase>
              <conf:linkbase><xsl:value-of select="concat($schema,'-',$year,'1231')"/>_lab.xml</conf:linkbase>
              <conf:linkbase><xsl:value-of select="concat($schema,'-',$year,'1231')"/>_def.xml</conf:linkbase>
              <conf:schema><xsl:value-of select="concat($schema,'-',$year,'1231')"/>.xsd</conf:schema>
            </conf:data>
            <conf:result>
              <conf:assert severity="err" num="60535" name="Incompatible-Numeric-Type-And-Unit" frd="cp"/>
            </conf:result>
          </conf:variation>
        </xsl:for-each>
       
      </conf:testcase>
    </xsl:result-document>
    <xsl:result-document href="{$good}.xml" method="xml" encoding="UTF-8" indent="yes" exclude-result-prefixes="#all">
      <xsl:element name="xbrl" namespace="{$nsXbrli}">
        <xsl:call-template name="prologue"/>
        <xsl:for-each-group select="xs:element/xs:annotation/xs:documentation[@source='good']/*" group-by="substring-after(@id,'__')">
          <xsl:element name="unit">
            <xsl:attribute name="id" select="current-grouping-key()"/>
            <xsl:copy-of select="*" copy-namespaces="no"/>
          </xsl:element>
        </xsl:for-each-group>
        <xsl:for-each select="xs:element">
          <xsl:variable name="element" select="@name"/>
          <xsl:for-each select="xs:annotation/xs:documentation[@source='good']/*">
            <xsl:element name="{$prefix}:{$element}" namespace="{$nsTarget}">
              <xsl:attribute name="unitRef" select="substring-after(@id,'__')"/>
              <xsl:attribute name="contextRef">_</xsl:attribute>
              <xsl:attribute name="nil" namespace="http://www.w3.org/2001/XMLSchema-instance">true</xsl:attribute>
            </xsl:element>
            <xsl:element name="{$prefix}:Derived{$element}" namespace="{$nsTarget}">
              <xsl:attribute name="unitRef" select="substring-after(@id,'__')"/>
              <xsl:attribute name="contextRef">_</xsl:attribute>
              <xsl:attribute name="nil" namespace="http://www.w3.org/2001/XMLSchema-instance">true</xsl:attribute>
            </xsl:element>
          </xsl:for-each>
        </xsl:for-each>
      </xsl:element>
    </xsl:result-document>
    <xsl:for-each select="xs:element/xs:annotation/xs:documentation[@source='nogood']/*">
      <xsl:variable name="seq" select="format-number(position()+1,'000')"/>
      <xsl:variable name="id" select="concat($us,$seq,'ng')"/>
      <xsl:variable name="base" select="concat('e60535',$seq,'ng-',concat($year,'1231'))"/>
      <xsl:variable name="nogood" select="concat($base,'.xml')"/>
      <xsl:result-document href="{$nogood}" method="xml" encoding="UTF-8" indent="yes" exclude-result-prefixes="#all">
        <xsl:element name="xbrl" namespace="{$nsXbrli}">
          <xsl:call-template name="prologue"/>
          <xsl:element name="unit">
            <xsl:attribute name="id" select="substring-after(@id,'__')"/>
            <xsl:copy-of select="*" copy-namespaces="no"/>
          </xsl:element>
          <xsl:element name="{$prefix}:{ancestor::xs:element/@name}" namespace="{$nsTarget}">
            <xsl:attribute name="unitRef" select="substring-after(@id,'__')"/>
            <xsl:attribute name="contextRef">_</xsl:attribute>
            <xsl:attribute name="nil" namespace="http://www.w3.org/2001/XMLSchema-instance">true</xsl:attribute>
          </xsl:element>
        </xsl:element>
      </xsl:result-document>
    </xsl:for-each>   
  </xsl:template>
  <xsl:template name="prologue">
    <xsl:namespace name="" select="$nsXbrli"/>
    <xsl:namespace name="xbrli" select="$nsXbrli"/>
    <xsl:namespace name="link" select="$nsLink"/>
    <xsl:namespace name="xlink" select="$nsXlink"/>
    <xsl:namespace name="{$prefix}" select="$nsTarget"/>
    <xsl:namespace name="iso" select="$nsIso"/>
    <xsl:namespace name="utr">http://www.xbrl.org/2009/utr</xsl:namespace>
    <xsl:namespace name="xsi">http://www.w3.org/2001/XMLSchema-instance</xsl:namespace>
    <xsl:namespace name="local">local</xsl:namespace>
    <xsl:namespace name="dei" select="$nsDei"/>
    <link:schemaRef xlink:type="simple" xlink:href="{$schema}-{$year}1231.xsd"/>
    <context id="_">
      <entity>
        <identifier scheme="http://www.sec.gov/CIK">9876543210</identifier>
      </entity>
      <period>
        <startDate>
          <xsl:value-of select="concat($fyear,'-01-31')"/>
        </startDate>
        <endDate>
          <xsl:value-of select="concat($fyear,'-12-31')"/>
        </endDate>
      </period>
    </context>
    <xsl:element name="DocumentType" namespace="{$nsDei}"><xsl:attribute name="contextRef">_</xsl:attribute><xsl:text>8-K</xsl:text></xsl:element>
    <xsl:element name="AmendmentFlag" namespace="{$nsDei}"><xsl:attribute name="contextRef">_</xsl:attribute><xsl:text>false</xsl:text></xsl:element>
    <xsl:element name="EntityRegistrantName" namespace="{$nsDei}">
      <xsl:attribute name="contextRef">_</xsl:attribute>
      <xsl:value-of select="concat('ng_',ancestor::xs:element/@name,$us,substring-after(@id,'__'))"/>
    </xsl:element>
    <xsl:element name="EntityCentralIndexKey" namespace="{$nsDei}"><xsl:attribute name="contextRef">_</xsl:attribute>9876543210</xsl:element>
    <xsl:element name="DocumentPeriodEndDate" namespace="{$nsDei}">
      <xsl:attribute name="contextRef">_</xsl:attribute>
      <xsl:value-of select="concat($fyear,'-12-31')"/>
    </xsl:element>
    <xsl:element name="EntityEmergingGrowthCompany" namespace="{$nsDei}"><xsl:attribute name="contextRef">_</xsl:attribute><xsl:text>false</xsl:text></xsl:element>
  </xsl:template>
  <xsl:template match="xs:annotation[parent::xs:element]" mode="clean"/>
  <xsl:template match="xs:annotation[parent::xs:schema]" mode="clean">
    <xsl:copy>
      <xsl:copy-of select="xs:appinfo"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="xs:*" mode="clean">
    <xsl:copy>
      <xsl:apply-templates select="@*" mode="clean"/>
      <xsl:apply-templates select="*" mode="clean"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="@*" mode="clean">
    <xsl:copy-of select="."/>
  </xsl:template>
 
  
 
</xsl:stylesheet>
