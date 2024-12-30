// logbrowserfunc.js

selectedItem=0;

function FindEnclosingDiv(elt)
{
    // Traverse parents of elt until a div is found.  Return the div
    curElt = elt;
    level = 0;
    while (curElt.nodeName != "DIV")
    {
        //alert("Not yet: " + curElt.nodeName);
        curElt = elt.parentNode;
        level++;
        
        if (level > 5)
        {
            return 0;
        }
    }

    return curElt;
}

function GetId()
{
    return selectedItem;
}

function SetId(event)
{
    //alert("event type: " + event.type);
    //alert("event target: " + event.target);
    //alert("event node name: " + event.target.nodeName);
    enclosingDiv = FindEnclosingDiv(event.target);
    
    if (enclosingDiv != 0)
    {
        //alert("Found enclosing DIV.  Class: " + enclosingDiv.className + "  Id: " + enclosingDiv.id);
        thisId = enclosingDiv.id;
        
        if (thisId != 0)
        {
            //document.getElementById(thisId).style.backgroundColor='#b0c4de';
            selectedItem=thisId;
        }
    }
}

function UnhighlightLog(event)
{
    if (event.target.nodeName != 0)
    {
        thisId = event.target.id;
        
        if (thisId != 0)
        {
            document.getElementById(thisId).style.backgroundColor='#ffffff';
        }
    }
}

function ScrollToElement(elementId)
{
    var selectedPosX = 0;
    var selectedPosY = 0;

    var theElement = document.getElementById(elementId);

    if (theElement != null)
    {
        while(theElement != null)
        {
            selectedPosX += theElement.offsetLeft;
            selectedPosY += theElement.offsetTop;
            theElement = theElement.offsetParent;
        }
                            		      
        window.scrollTo(0, selectedPosY);
    }
}
